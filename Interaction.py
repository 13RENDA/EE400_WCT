import csv
import time
from datetime import datetime

# Object to handle an interaction with subsystems to meet user requests
class Interaction:
  # Instantiation
  def __new__(cls, *args, **kwargs):
    return super().__new__(cls)
  
  # Initialization
  def __init__(self, response_delay_millis, room_id_dict, room_info_dict):
    # start time of iteraction operations
    self.start_time = datetime.utcnow()
    
    # time to delay response output by in order more naturtally mirror human comprehension/action
    # must in terms of seconds for time.sleep() function
    self.response_delay_secs = (float)response_delay_millis / 1000
    
    # {room_number : room_id} dictionary. Intended to be inialized from "DialogEngine.room_id_dict"
    self.room_id_dict = room_id_dict
    
    # {room_number : room_id} dictionary. Intended to be inialized from "DialogEngine.room_info_dict"
    self.room_info_dict = room_info_dict
    
    # string to contain the actions taken; to be added to with each Interaction action function call 
    self.actions_performed = ""
    
  ################################################################################################# 
  ############# Helper functions for system interfacing with with subsystems ######################   
    
   # put the "TODO" functions, from below, in this section
    
  ################################################################################################# 
  ############# Acrtion functions to interact with subsystems for user requests ###################
    
  # Function to log an unsucesful interaction with a user--no follow-on system actions occur
  def unsuccesful():
    self.actions_performed += "unsucessful"
    
  # Function to send a room ID to car for dispatch  
  def guide_car(self, response, room_number):
    self.actions_performed += "guide-car action performed, "
    room_id = self.room_dict.get(room_number)
    # TODO function to get room_id from room_number dictionary
    # TODO insert function to send id to car ESP32
    time.sleep(self.response_delay_secs)
    return response + " " + room_number
    
  # Function to query room info data
  def room_info(self, response, room_number):
    self.actions_performed += "room information request action performed, "
    time.sleep(self.response_delay_secs)
    return response + self.room_info_dict.get(room_number)
  
  # Function to return available rooms, according to sensor data
  def room_avail(self, response):
    self.actions_performed += "room availability action performed, "
    # TODO function that grabs sensor info from network and assembled a string of available rooms;
    #      Sensor data should correspond to room IDs, then use self.room_id_dicyt to get room number
    #      when assembling the string
    time.sleep(self.response_delay_secs)
    return response + rooms_string
    
  ################################################################################################# 
  ############# Functions to end interaction and return interaction time data #####################
  
  def end(self)
    # Interaction end time
    end_time = datetime.utcnow()
  
    # Calculate the difference
    time_difference = end_time - self.start_time

    # Extract hours and minutes from time_difference
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes = remainder // 60

    # Format the start time
    start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")

    # Create the formatted time string
    formatted_time_string = f"{start_time_str}, {hours}:{minutes:02d}"

    # Return time and actions data strings
    return formatted_time_string, self.actions_performed

# Object to log interaction data to a csv file
# object instantiation creates a new .csv file with file name formatted as:
#     "log_session_beginning_<year>_<month>_H:M:S.csv"
class InteractionLogger:
  def __init__(self, pathname):
    # Ensure the pathname ends with a slash
    if not pathname.endswith('/'):
        pathname += '/'

    # Create the directory if it does not exist
    os.makedirs(pathname, exist_ok=True)

    # Get the current UTC time for the filename
    current_time = datetime.utcnow()
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    self.filename = f"{pathname}log_session_beginning_{formatted_time}.csv"

    # Open the file in write mode
    self.file = open(self.filename, mode='w', newline='', encoding='utf-8')
    self.writer = csv.writer(self.file, delimiter='|')

  def log_interaction(self, interaction_string):
    # Write the interaction string to the CSV file
    self.writer.writerow([interaction_string])

  def close_log(self):
    # Close the file
    self.file.close()