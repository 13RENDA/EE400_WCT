# Responses object that holds dictionaries of expected input prompts, their synonyms,
# and their mapped responses

# dependencies: 
import csv
import re
from word2number import w2n

class DialogEngine:

  ################################################################################################# 
  ############# Construction and initialization of object from response data files ################

  # class constructor
  def __new__(cls, *args, **kwargs):
    return super().__new__(cls)

  # initialization builds dictionaries from input synonym and reponse files
  #   input synonym file format:    line:  "<synonym> <prompt>"
  #   input reponse file format:    line:  "<prompt> <syn> <syn> ... <syn>"
  def __init__(self, 
               input_response_file_name, 
               input_syn_file_name,
               input_room_id_file_name,
               input_room_info_file_name):
    self.syn_file_name = input_syn_file_name
    self.resp_file_name = input_response_file_name
    self.syn_dict = self.build_syn_dict(input_syn_file_name)
    self.resp_dict = self.build_response_dict(input_response_file_name)
    self.room_id_dict = self.build_syn_dict(input_room_id_file_name)
    self.room_info_dict = self.build_response_dict(input_room_info_file_name)

  # build {input_prompt : response} dictionary from .txt file containing response
  # dictionary, each line formatted as "<input_prompt> <response, actions>"
  def build_response_dict(cls, input_response_file_name):
    resp_dict = {}
    with open(input_response_file_name, mode='r', newline='', encoding='utf-8') as csvfile:
      csvreader = csv.reader(csvfile, delimiter='|')
      for row in csvreader:
        if len(row) >= 3:
          # Assuming the first column is the prompt and the second is the response
          prompt = row[0].strip()
          response = row[1].strip()
          actions = [int(num) for num in row[2:]] # convert string nums read from .csv to ints
          resp_dict[prompt] = response, actions
    return resp_dict

  # build {synonym : input_prompt} dictionary from .txt file containing input-synonyms
  # dictionary data, each line formatted as "<prompt> <input_syn1 input_syn2..>"
  def build_syn_dict(cls, input_syn_file_name):
    syn_dict = {}
    with open(input_syn_file_name, mode='r', newline='', encoding='utf-8') as csvfile:
      csvreader = csv.reader(csvfile, delimiter='|')
      for row in csvreader:
        if len(row) >= 2:
          # The first item is the prompt and the rest are synonyms
          prompt = row[0].strip()
          synonyms = [syn.strip() for syn in row[1:]]
          for syn in synonyms:
            syn_dict[syn] = prompt
    return syn_dict
  
  # build {synonym : input_prompt} dictionary from .txt file containing input-synonyms
  # dictionary data, each line formatted as "<prompt> <input_syn1 input_syn2..>"
  def build_room_info_dict(cls, input_room_id_file_name):
    id_dict = {}
    with open(input_room_id_file_name, mode='r', newline='', encoding='utf-8') as csvfile:
      csvreader = csv.reader(csvfile, delimiter='|')
      for row in csvreader:
        if len(row) >= 2:
          room_number = row[0].strip()
          room_id = row[1].strip()
          id_dict[room_number] = room_id
    return id_dict
  
  # build {synonym : input_prompt} dictionary from .txt file containing input-synonyms
  # dictionary data, each line formatted as "<prompt> <input_syn1 input_syn2..>"
  def build_room_info_dict(cls, input_room_info_file_name):
    info_dict = {}
    with open(input_room_info_file_name, mode='r', newline='', encoding='utf-8') as csvfile:
      csvreader = csv.reader(csvfile, delimiter='|')
      for row in csvreader:
        if len(row) >= 2:
          room = row[0].strip()
          info = row[1]
          info_dict[room] = info
    return info_dict
  
  ################################################################################################# 
  ################ functions to generate data text files from object dictionaries ################# 

  # function to save prompts and their responses to .csv file called by stored syn_file_name
  def responses_to_file(self):
    with open(self.resp_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
      writer = csv.writer(csv_file, delimiter='|')

      for prompt in self.resp_dict:
          # Create a row with the prompt followed by its synonyms
          response, actions = self.resp_dict.get(prompt)
          row = [prompt] + [response] + [actions]
          writer.writerow(row)

  # function to save prompts and their synonyms to a different .csv file called by input name
  def responses_to_new_file(self, output_resp_file_name):
    with open(output_resp_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
      writer = csv.writer(csv_file, delimiter='|')

      for prompt in self.resp_dict:
          # Create a row with the prompt followed by its synonyms
          response, actions = self.resp_dict.get(prompt)
          row = [prompt] + [response] + [actions]
          writer.writerow(row)

  # function to save prompts and their synonyms to .csv file called by stored syn_file_name
  def synonyms_to_file(self):
    # group synonyms by prompt
    prompt_syns = _invert_str_dict(self.syn_dict)

    with open(self.syn_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
      writer = csv.writer(csv_file, delimiter='|')

      for prompt in prompt_syns:
          # Create a row with the prompt followed by its synonyms
          row = [prompt] + prompt_syns.get(prompt)
          writer.writerow(row)

  # function to save prompts and their synonyms to a different .csv file called by input name
  def synonyms_to_new_file(self, output_syn_file_name):
    # group synonyms by prompt
    prompt_syns = _invert_str_dict(self.syn_dict)

    with open(output_syn_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
      writer = csv.writer(csv_file, delimiter='|')

      for prompt in prompt_syns:
          # Create a row with the prompt followed by its synonyms
          row = [prompt] + prompt_syns.get(prompt)
          writer.writerow(row)

  ################################################################################################# 
  ### functions to parse input for (prompts, numbers) to use with object and give output ##########
  
  # parses a string for a three digit number. if a three digit number is not found, returns none
  def parse_number_words(self, input_string):
    # Replace 'oh' or 'o' with 'zero' for clarity in parsing
    input_string = input_string.replace(" oh ", " zero ").replace(" o ", " zero ")

    # Regular expression to find number words
    number_word_pattern = re.compile(r"\b(one|two|three|four|five|six|seven|eight|nine|zero|ten|"
                                     r"eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|"
                                     r"eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|"
                                     r"eighty|ninety|hundred|thousand)\b", re.IGNORECASE)

    number_words = number_word_pattern.findall(input_string)

    # Check if the number of words is between 2 and 3
    if len(number_words) < 2 or len(number_words) > 3:
      return None

    try:
      # Parse the hundreds place
      hundreds = w2n.word_to_num(number_words[0]) * 100

      # Parse the tens and ones places
      tens_ones = w2n.word_to_num(' '.join(number_words[1:])) if len(number_words) > 1 else 0

      # Combine the values to form a three-digit number
      three_digit_number = hundreds + tens_ones

      # Check if the number is indeed a three-digit number
      if 100 <= three_digit_number <= 999:
        return three_digit_number
      else:
        return None
    except ValueError:
      return None
  
  def parse_for_prompt(self, input_string, response_dict):
    found_prompt_list = [prompt for prompt in response_dict if prompt in input_string]
    if len(found_prompt_list) != 1:
      return None
    else: 
      return found_prompt_list[0]

  ################################################################################################# 
  ################## functions to interact with the response object ###############################

  # Return format: (<response_string>, <response_actions_ints_list>, <response_int>)
  # Returns response for prompt phrase and any int number in found phrase
  # If prompt word is not mapped to a response, checks synonyms 
  # else, eturns "unkn"
  # returns None for number if no number found
  def response(self, phrase):
    number = self.parse_number_words(phrase)
    #TODO debug line
    print("number found: ", number)
    
    # parse input against possible prompts
    prompt = self.parse_for_prompt(phrase, self.resp_dict)
    
    # if prompt not found in phrase, parse against synonyms for prompts
    if prompt is None:
      prompt = self.parse_for_prompt(phrase, self.syn_dict)
      
    #TODO debug line
    print("prompt found: ", prompt) 
    
    # If synonym still not found, return None, otherwise convert synonym to corresponding prompt
    if prompt is None:
      return "unkn", None, None
    else:
    # Use the found prompt, or default to itself if not in syn_dict
      prompt = self.syn_dict.get(prompt, prompt)  

    # Try to get the response and actions from the dictionary
    result = self.resp_dict.get(prompt)

    # Check if result is not None
    if result is not None:
      response, actions = result
    else:
      # Handle the case where the prompt is not found
      response, actions = "No response found", None

    # Return tuple of response string, response actions ints lists, and response parsed number int
    return response, actions, number
    
  # prints object's prompts and associated responses
  def print_responses(self):
    for prompt in self.resp_dict:
      response, actions = self.resp_dict.get(prompt)
      print("(prompt) "+prompt+" | (response) "+response," | (actions sequence", actions)
    return 

  # prints object's prompts and their synonyms
  def print_synonyms(self):
    # group synonyms by prompt
    prompt_syns = _invert_str_dict(self.syn_dict)

    # prints "prompt: [syns]"
    for prompt in prompt_syns.keys():
      string = "\'" +str(prompt) + "\' :"
      for syn in prompt_syns.get(prompt):
        string += " \'" + syn + "\'"
      print(string)
  
  ################################################################################################# 
  ######## functions to update response object information (prompt, synonyms, responses) ##########

  # add prompt, associated response, and a list of prompt synonyms
  # if the prompt word already exists, prints "prompt already associated, no action taken"
  # if any synonyms are already associated with other keywors, will print "[<syn>, <sun>, ...] already taken"
  def add_prompt(self, prompt, response, list_actions, list_synonyms):
    if prompt in list(self.resp_dict.keys()):
      print("prompt {prompt} already associated, no action taken")
      return
    else:
      self.resp_dict[prompt] = (response, list_actions)
      for syn in list_synonyms:
        self.add_synonym(prompt, syn)
      return

  # function to change old prompt to new prompt in dictionaries, updating mapping
  # {<synonym> : <newprompt>} and {<newprompt> : <response>}
  def update_prompt(self, old_prompt, new_prompt):
    synonyms = list(self.syn_dict.keys())
    prompts = list(self.resp_dict.keys())
    # update prompt-response pairs. If prompt not in dicts, print error, return
    if old_prompt in prompts:
      self.resp_dict[new_prompt] = self.resp_dict.pop(old_prompt)
    else:
      print("The key {old_prompt} does not exist in the dictionary.")

    # if the new prompt exists as a synonym for another prompt, removes new prompt
    # phrase from synonym dictionary
    if new_prompt in synonyms:
      self.syn_dict.pop(new_prompt)
    
    # update synonym key-value pairs
    syns_to_update = [syn for syn, prompt in self.syn_dict.items() if prompt == old_prompt]

    # Update the value for each of those keys
    for syn in syns_to_update:
      self.syn_dict[syn] = new_prompt
  
  # remove a prompt, associated response, and associated synonyms
  # prints "prompt has no assocated response" if prompt does not exist
  def remove_prompt(self, prompt):
    prompts = list(self.resp_dict.keys())
    # if prompt exists, remove it
    if prompt in prompts:
      # remove synonyms associated with prompt
      syns_to_remove = [syn for syn, prompt_ in self.syn_dict.items() if prompt_ == prompt]

      # Update the value for each of those keys
      for syn in syns_to_remove:
        self.syn_dict.pop(syn)
    # prompt does not exist
    else:
      print("The key {prompt} does not exist in the dictionary.")

  # update response for input word. word must either exist as a prompt or
  # a prompt's synonym to be associated in dictionaries
  # if list_new actions is an empty list, no updates to actions are made,
  # otherwise the actions are updated to the input list
  def update_response(self, prompt_or_syn, response, list_new_actions):
    len_new_actions = len(list_new_actions)
    if prompt_or_syn in self.resp_dict:
      prompt = prompt_or_syn
    else:
      prompt = self.syn_dict.get(prompt_or_syn)
      if (prompt == 'None'): 
        print("The key {prompt_or_syn} does not exist in the dictionary.")
        return
    curr_response, actions = self.resp_dict.get(prompt)
    if len_new_actions != 0:
      actions = list_new_actions
    self.resp_dict[prompt] = response, actions
    return
  
  # add a synonym for a prompt
  # prints "prompt {prompt} has no assocated response" if prompt does not exist
  # prints "Synonym already associated with with prompt {other_prompt}" if synonym
  #        already associated with another existing prompt
  def add_synonym(self, prompt, synonym):
    prompts = list(self.resp_dict.keys())
    synonyms = list(self.syn_dict.keys())
    if prompt in prompts:
      if synonym in synonyms:
        other_prompt = self.syn_dict.get(prompt)
        print("Synonym already associated with with prompt {other_prompt}")
        return
      else:
        self.syn_dict[synonym] = prompt
        return
    else:
      print("prompt {prompt} has no assocated response (not in dictionary)")
      return

  # remove a synonym for a prompt
  # prints "Synonym {synonym} : {prompt} association does not exist" if pair not found
  #        this protects against unintended removing of a synonym pairing with a 
  #        different prompt
  def remove_synonym(self, prompt, synonym):
    if (self.syn_dict.get(synonym) != prompt):
      print("Synonym {synonym} : {prompt} association does not exist")
      return
    else:
      self.syn_dict.pop(synonym)
      return

  # updates {<synonym> : <new_prompt>} pairing for an existing synonym, prints message
  #         showing change from old prompt to other_prompt
  # prints "Synonym {synonym} does not exist" if synonym not already associated
  # prints "prompt {prompt} not in dictionary" if prompt not associated in response onj
  def update_synonym(self, synonym, other_prompt):
    prompts = list(self.resp_dict.keys())
    synonyms = list(self.syn_dict.keys())
    if synonym in synonyms:
      if other_prompt not in prompts:
        print("prompt {prompt} not in dictionary")
        return
      else:
        old_prompt = self.syn_dict.pop(synonym)
        self.syn_dict[synonym] = other_prompt
        print("Synonym {synonym} now associated with {other_prompt}" 
              + "(used to be associated with {old_prompt})")
        return
    else: 
      print("Synonym {synonym} does not exist")
      return
################################################################################################# 
################################### general helper functions ####################################

# inverts a dictionary so that output dict uses unique value of original dictionary as keys and
# contains a list of original keys associated with unique val as the value in the new dict
def _invert_str_dict(input_dict):
  inverted_dict = {}
  for key, value in input_dict.items():
      # If the value already exists as a key in the inverted dictionary,
      # append the current key to its list.
      if value in inverted_dict:
          inverted_dict[value].append(key)
      else:
          # Otherwise, create a new entry with this value as the key
          # and the current key as the first item in a list.
          inverted_dict[value] = [key]
  return inverted_dict