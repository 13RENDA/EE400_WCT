# object to generate wave files from system audio input and play to system audio output

import subprocess
import signal

class AudioHandler:
  # class constructor
  def __new__(cls, *args, **kwargs):
    return super().__new__(cls)

  # initializer
  # ffmpeg 
  def __init__(self, input_device_index):
    self.input_device_index = input_device_index
    self.process = []
    
  # Function to start recording
  # input_device_index refers to the "avfoundation" device for use by ffmpeg (example ":2")
  def start_recording(self, filename):
    ffmpeg_command = [
        "ffmpeg",
        "-f", "avfoundation",  # macOS input format
        "-ar", "16000",        # Set audio sample rate to 16000 Hz
        "-ac", "1",            # Set number of audio channels to 1 (mono)
        "-i", self.input_device_index,  # Input device index, replace with your microphone's index
        "-acodec", "pcm_s16le", # Set audio codec to PCM 16-bit
        "-y",                  # Overwrite output files without asking
        filename               # Output filename
    ]
    self.process.append(subprocess.Popen(ffmpeg_command, 
                                         stdin=subprocess.PIPE, 
                                         stdout=subprocess.PIPE, 
                                         stderr=subprocess.PIPE))

  # Function to stop recording
  def stop_recording(self):
    self.process[0].send_signal(signal.SIGINT)  # Send an interrupt signal
    self.process[0].wait()
    self.process = []

  # function to play audio file "filename"
  def play_audio(self, file_name):
    command = ["ffplay", "-nodisp", "-autoexit", file_name]
    subprocess.run(command)

class AudioHandlerLinux:
    # class constructor
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    # initializer
    def __init__(self, input_device_index):
        self.input_device_index = input_device_index
        self.process = []
    
    # Function to start recording
    # input_device_index refers to the ALSA device for use by ffmpeg (example "hw:0")
    def start_recording(self, filename):
        ffmpeg_command = [
            "ffmpeg",
            "-f", "alsa",          # Linux input format
            "-ar", "16000",        # Set audio sample rate to 16000 Hz
            "-ac", "1",            # Set number of audio channels to 1 (mono)
            "-i", self.input_device_index,  # Input device index, replace with your microphone's index
            "-acodec", "pcm_s16le", # Set audio codec to PCM 16-bit
            "-y",                  # Overwrite output files without asking
            filename               # Output filename
        ]
        self.process.append(subprocess.Popen(ffmpeg_command, 
                                             stdin=subprocess.PIPE, 
                                             stdout=subprocess.PIPE, 
                                             stderr=subprocess.PIPE))

    # Function to stop recording
    def stop_recording(self):
        self.process[0].send_signal(signal.SIGINT)  # Send an interrupt signal
        self.process[0].wait()
        self.process = []

    # function to play audio file "filename"
    def play_audio(self, file_name):
        command = ["ffplay", "-nodisp", "-autoexit", file_name]
        subprocess.run(command)
