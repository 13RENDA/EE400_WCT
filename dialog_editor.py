# client script to populate interaction prompt, response, and action data set, output as 
# .csv files
import DialogEngine as de
import csv

mode_select = 0

###############################################################################################
#################### Helper functions #########################################################
def print_action_codes():
  with open("action_codes.csv", newline='') as legend:
    reader = csv.reader(legend)
  for row in reader:
    print(row[0]+" : "+row[1])


################## Intro and mode selection #####################################################
print("This a dialog database editor utility. It can be used to modify or generate"
      +".csv files containing prompt, prompt-synonyms, response, and system actions data"
      +"for use by the chat-interactive system\n\n")
while True:
  mode_select = input("What would you like to do (please enter a number):\n"
                      + "__________________________________________________\n"
                      +"1. Modify existing files\n"
                      +"2. Create new files\n"
                      +"3. Review files\n")
  if (mode_select == 1 or mode_select == 2 or mode_select == 3):
    break
  else:
    print("please enter '1', '2', or '3'")

if mode_select == 2:
  resp_name = input("please enter new prompt-response file name (ex. <filename>.csv): ")  
  syn_name = input("please enter new prompt-synonym file name (ex. <filename>.csv): ") 
else:
  resp_name = input("please enter existing prompt-response file name (ex. <filename>.csv): ")  
  syn_name = input("please enter existing prompt-synonym file name (ex. <filename>.csv): ") 

################### New file creation ########################################################
resp_file = csv.writer(resp_name)
syn_file = csv.writer(syn_name)

################### Dialog object ############################################################
dialog = de.DialogEngine(resp_name, syn_name)

################### Data review mode #########################################################
if mode_select == 3:
  print("PROMPT | RESPONSES | ACTIONS CODE SEQUENCE\n"
        +"__________________________________________")
  dialog.print_responses()
  print("\n\n")
  print("PROMPT | SYNONYMS\n"
        +"__________________________________________")
  dialog.print_synonyms()
  print("CODE | ACTION\n"
        +"__________________________________________")
  print_action_codes()
  
################### Data input/update mode #########################################################
else:
  while True:
    print ()