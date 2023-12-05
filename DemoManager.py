# Demo system manager

import AudioHandler as ah
import AudioTextTransformer as at
import DialogEngine as de
import KeyboardActionListener as kal
import Interaction
import time


# TODO: determine and insert model file/path names for deepspeech and ttl instantiation
 
# audio input device index--> use "ffmpeg -f avfoundation -list_devices true -i" command
#                             in linux terminal to get indices associate AV IO devices
#                             spice input withh ":<index number>"
system_audio_in_index = ":1"
deepspeech_model_filename = ""
deepspeech_scorer_filename = ""
tts_model_path = ""
tts_config_path = ""
tts_vocoder_path = ""
tts_vocoder_config_path = ""
audio_in_file_name = "request.wav"
audio_out_file_name = "response.wav"
log_file_path = "./"
response_delay_millis = 500. # must be double value

# set up system objects
dialog = de.DialogEngine("./demo_files/demo_responses.csv", 
                         "./demo_files/demo_synonyms.csv",
                         "./demo_files/demo_room_ids.csv",
                         "./demo_files/demo_room_info.csv")
audio = ah.AudioHandler(system_audio_in_index)
att = at.AudioTextTransformer(deepspeech_model_filename, 
                               deepspeech_scorer_filename, 
                               tts_model_path, 
                               tts_config_path, 
                               tts_vocoder_path, 
                               tts_vocoder_config_path,
                               audio_out_file_name)
logger = Interaction.InteractionLogger(log_file_path)
keylistener = kal.KeyActionListener(audio.start_recording(audio_in_file_name),
                                    audio.stop_recording(),
                                    quit = True)

# program flow variables
quit = False
interaction_complete = False

# function to set program quit condition
def quit_program():
  print("Quitting program")
  quit = True
  
# function that closes a completed succesful interaction by calling passed interaction objects's and 
# logger's corresponding functions
def complete_interaction(text_response, interaction_object):
  log_info = interaction_object.end()
  logger.log_interaction(log_info)
  time.sleep(response_delay_millis / 1000)
  audio_file_name = at.text2audio(text_response)
  ah.play_audio(audio_file_name)
  # print(text_response)
    
  
# re-initiates ineraction if previous input from user is not comprehensible  
def get_new_request():
  time.sleep(response_delay_millis / 1000)
  # print("I'm sorry, I didn't understand your last request. Let's try again. How can I help you?")
  att.text2audio("I'm sorry, I didn't understand your last request. Let's try again. How can I help you?")
  interaction_complete == True
  
# MAIN SYSTEM RESPONSE LOGIC  
# function to respond to request upon releasing space bar
def process_request():
  keylistener.suspend()
  input_audio_file = audio.stop_recording()
  request_text = att.audio2text(input_audio_file)
  initial_response, room_number, action = dialog.response(request_text)
  
  # if request not understood
  if (text_response == "unkn"):
    interaction = Interaction.Interaction(response_delay_millis,
                                          dialog.room_id_dict, 
                                          dialog.room_info_dict)
    interaction.unsuccessful()
    log_info = interaction.end()
    logger.log_interaction(log_info)
    get_new_request()
  
  # response generated with no follow on action necessary
  elif (action == 0):
    # TODO change print statement to MozillaTTL function to generate audio, and then call "audio.play_audio()"
    print(text_response)
    
  # response necessitates another interaction with the the user
  elif (action == 1):
    # TODO change print statement to MozillaTTL function to generate audio, and then call "audio.play_audio()"
    print(text_response)
    
  # response generated with request for sensor info
  elif (action == 2):
    interaction = Interaction.Interaction(response_delay_millis,
                                          dialog.room_id_dict, 
                                          dialog.room_info_dict)
    text_response = interaction.room_avail(initial_response)
    complete_interaction(text_response, interaction)

  # response generated with request of information for specific room 
  elif (action == 3):
    interaction = Interaction.Interaction(response_delay_millis,
                                          dialog.room_id_dict, 
                                          dialog.room_info_dict)
    text_response = interaction.room_info(initial_response, room_number)
    complete_interaction(text_response, interaction)

  # response generated with request for car-guide
  elif (action == 4):
    interaction = Interaction.Interaction(response_delay_millis,
                                          dialog.room_id_dict, 
                                          dialog.room_info_dict)
    text_response = interaction.guide_car(initial_response, room_number)
    complete_interaction(text_response, interaction)
  
# KEYBOARD INPUT LISTENER  
# pressing 'space' starts recording
# releasing 'space' stops recording
# pressing 'q' set program quit condition
# access audio file generated by releasing 'space' with "keylistener.stop_output"
keylistener = kal.KeyActionListener(audio.start_recording(audio_in_file_name),
                                    process_request(),
                                    quit_program())

# MAIN LOOP
while (quit == False):
  interaction_complete = False
  keylistener.start()
  print("Hold down 'space' to record input\n\n(press q to quit)\n")
  while (True):
    if interaction_complete == True:
      break
  
  