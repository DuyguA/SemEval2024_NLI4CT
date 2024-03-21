import json
from poe_api_wrapper import PoeApi

token = "MY_TOKEN"
client = PoeApi(token)

# set of bots falcon_40b_beta, mixtral-8x7b-chat, acouchy, gemini-pro, a2, chinchilla, beaver  
bot = "llama_2_70b_chat"
chatcode = "MY_CHATCODE"



with open("all_trials.json", "r") as injs1:
    all_trials = json.loads(injs1.read())


def fetch_text(trial_id, section):
  return all_trials[trial_id][section]

data_folder = "../"

devset = data_folder + "dev.json"


with open(devset, "r") as infile:
    devsetjs = json.loads(infile.read())




single_prompt = "Below find {section_name} section of the primary trial of a clinical trial. Infer if the following statement entails from the given trial information. Answer should be either entailment or contradiction. Please justify the answer based on numbers.\nPRIMARY TRIAL {section_name2}:\n{trial_value}\nSTATEMENT: {statement}"

comparison_prompt = "Below find {section_name} sections of a primary trial and a secondary trial belonging to same clinical trial. Infer if the following statement entails from the given trial information. Answer should be either entailment or contradiction. Please justify the answer based on numbers.\nPRIMARY TRIAL {section_name2}:\n {trial_value1}\nSECONDARY TRIAL {section_name2}:\n {trial_value2}\nSTATEMENT:\n{statement}"


outfilename = "results_devset/" + bot + ".jsonl"
ids_file = "results_devset/ids.txt"
ready_ids = open(ids_file, "r").read().split("\n")
ready_ids = ready_ids[:-1]

with open(outfilename, "a+") as ofile:
  for devkey, minijs in devsetjs.items():
    if devkey in ready_ids:
      continue
    typ = minijs["Type"]
    sect = minijs["Section_id"]
    primary = minijs["Primary_id"]
    statement = minijs["Statement"]
    if typ == "Comparison":
      secondid = minijs["Secondary_id"]
      primary_text = fetch_text(primary, sect)
      secondary_text = fetch_text(secondid, sect)
      prompt = comparison_prompt.format(section_name=sect, section_name2=sect.upper(), trial_value1=primary_text, trial_value2=secondary_text, statement=statement)
    elif typ == "Single":
      primary_text = fetch_text(primary, sect)
      prompt = single_prompt.format(section_name=sect, section_name2=sect.upper(), trial_value=primary_text, statement=statement)
    #print(prompt)
    #print("----------------------")
    for chunk in client.send_message(bot, prompt, chatCode=chatcode):
      pass
    result = chunk["text"]
    print(prompt)
    print("-----------------------")
    print(result)
    print("-----------------------")
    outdict = {"id": devkey, "result": result}
    ojs = json.dumps(outdict)
    ofile.write(ojs + "\n")
