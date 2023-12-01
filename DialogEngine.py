# Responses object that holds dictionaries of expected input prompts, their synonyms,
# and their mapped responses

# dependencies: 
import csv

class DialogEngine:

  ################################################################################################# 
  ################ Construction and initialization of info from response data file ################

  # class constructor
  def __new__(cls, *args, **kwargs):
    return super().__new__(cls)

  # initialization builds dictionaries from input synonym and reponse files
  #   input synonym file format:    line:  "<synonym> <prompt>"
  #   input reponse file format:    line:  "<prompt> <syn> <syn> ... <syn>"
  def __init__(self, input_response_file_name, input_syn_file_name):
    self.syn_file_name = input_syn_file_name
    self.resp_file_name = input_response_file_name
    self.syn_dict = self.build_syn_dict(input_syn_file_name)
    self.resp_dict = self.build_response_dict(input_response_file_name)

  # build {synonym : input_prompt} dictionary from .txt file containing input-synonyms
  # dictionary data, each line formatted as "<prompt> <input_syn1 input_syn2..>"
  def build_syn_dict(cls, input_syn_file_name):
    syn_dict = {}
    with open(input_syn_file_name, mode='r', newline='', encoding='utf-8') as csvfile:
      csvreader = csv.reader(csvfile)
      for row in csvreader:
        if len(row) >= 2:
          # The first item is the prompt and the rest are synonyms
          prompt = row[0].strip()
          synonyms = [syn.strip() for syn in row[1:]]
          for syn in synonyms:
            syn_dict[syn] = prompt
    return syn_dict

  # build {input_prompt : response} dictionary from .txt file containing response
  # dictionary, each line formatted as "<input_prompt> <response>"
  def build_response_dict(cls, input_response_file_name):
    resp_dict = {}
    with open(input_response_file_name, mode='r', newline='', encoding='utf-8') as csvfile:
      csvreader = csv.reader(csvfile)
      for row in csvreader:
        if len(row) >= 3:
          # Assuming the first column is the prompt and the second is the response
          prompt = row[0].strip()
          response = row[1].strip()
          actions = row[2:]
          resp_dict[prompt] = (response, actions)
    return resp_dict

  ################################################################################################# 
  ################ functions to generate data text files from object dictionaries ################# 

  # function to save prompts and their responses to .csv file called by stored syn_file_name
  def responses_to_file(self):
    with open(self.resp_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
      writer = csv.writer(csv_file)

      for prompt in self.resp_dict:
          # Create a row with the prompt followed by its synonyms
          response, actions = self.resp_dict.get(prompt)
          row = [prompt] + [response] + [actions]
          writer.writerow(row)

  # function to save prompts and their synonyms to a different .csv file called by input name
  def responses_to_new_file(self, output_resp_file_name):
    with open(output_resp_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
      writer = csv.writer(csv_file)

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
      writer = csv.writer(csv_file)

      for prompt in prompt_syns:
          # Create a row with the prompt followed by its synonyms
          row = [prompt] + prompt_syns.get(prompt)
          writer.writerow(row)

  # function to save prompts and their synonyms to a different .csv file called by input name
  def synonyms_to_new_file(self, output_syn_file_name):
    # group synonyms by prompt
    prompt_syns = _invert_str_dict(self.syn_dict)

    with open(output_syn_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
      writer = csv.writer(csv_file)

      for prompt in prompt_syns:
          # Create a row with the prompt followed by its synonyms
          row = [prompt] + prompt_syns.get(prompt)
          writer.writerow(row)

  ################################################################################################# 
  ################## functions to interact with the response object ###############################

  # returns response for prompt word. 
  # If prompt word is not mapped to a response, checks synonyms 
  # else, eturns "unkn"
  def response(self, phrase):
    response = self.resp_dict.get(phrase)
    if response is None:
      prompt = self.syn_dict.get(phrase)
      if prompt is None:
        return "unkn"
      else:
        return self.resp_dict.get(prompt)
    return response
  
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
  ######## functions to update response object information (prompt, synonyms, responses) #########

  # add prompt, associated response, and a list of prompt synonyms
  # if the prompt word already exists, prints "prompt already associated, no action taken"
  # if any synonyms are already associated with other keywors, will print "[<syn>, <sun>, ...] already taken"
  def add_prompt(self, prompt, response, list_actions, list_synonyms):
    if prompt in list(self.resp_dict.keys()):
      print("prompt {prompt} already associated, no action taken")
      return
    else:
      self.resp_dict[prompt] = (response, list_synonyms)
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