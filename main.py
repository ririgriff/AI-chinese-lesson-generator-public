# main.py
import json
from pptx import Presentation
import datetime
import argparse

#from utils import testModule, getURL, cachecontent, load_json
from utils_LLM import askGPT, askImageGPT
from utils_createdecks import create_presentation, map_placeholder_index
from utils_data import script2FITB_vocab_files 


if __name__ == "__main__":

    today = datetime.date.today()

    # Lesson Configuration Parameters - EDIT AS NEEDED
    lesson_number = "1"        # used in output PPT file name
    story_number = "1"         # used in directory path
    title = "第一卷"            # used in title slides
    subtitle = "第一课：背书面包" # used in title slides
    num_images = 9

    # Input/Output file paths and names
    BASE_URL = "doraemon_content/story"+story_number+"/"

    # Json files - No need to edit
    script_path = BASE_URL+"final_json/aggregated_script.json"
    FITB_output_path = BASE_URL+"LLM_json/FITB_LLM.json"
    vocab_output_path = BASE_URL+"LLM_json/Vocab_LLM.json"
    FITB_final_path = BASE_URL+"final_json/FITB_final.json" # post-edit files
    vocab_final_path = BASE_URL+"final_json/Vocab_final.json"  # post-edit files

    # Powerpoint files - No need to edit
    template_path = "powerpoint_templates/doraemon_lesson_template_v1.pptx"
    output_path = "output_lesson/lesson"+lesson_number+"_" + str(today) +".pptx"
    indexdeck_output_path = "powerpoint_templates/template_with_index.pptx"

    # LLM request supporting files - No need to edit
    image2json_prompt = "prompt_templates/read_comicpage.txt" # for LLM
    script_response_format = "response_formats/comic_script.json" #for LLM


    parser = argparse.ArgumentParser()
    parser.add_argument("--createindexdeck", help="create a deck from template with index numbers for development use", action="store_true")
    parser.add_argument("--image2json", help="convert images to json files", action="store_true")
    parser.add_argument("--aggregatejson", help="aggregate json files into single json file", action="store_true")
    parser.add_argument("--supportingjson", help="create spawn json files for other slide formats", action="store_true")
    parser.add_argument("--createfinaldeck", help="Generate the final powerpoint deck", action="store_true")
    args = parser.parse_args()

    # -----------------> STEP X: CREATE INDEX DECK <------------------
    # Only need to run this if pptx template file changes and need to see the placeholder idx values
    # Output will be saved in "powerpoint_templates" folder
    if args.createindexdeck:
        print("Creating index decks")
        map_placeholder_index(template_path, indexdeck_output_path)


    # -----------------> STEP 1: IMAGE PROCESSING WITH LLM <------------------
    # Each page will require one call to OpenAI o1 model 
    # Save all images under folder "doraemon_content/story{x}/images/" 
    # images should be named as "1.png", "2.png" ...
    # outputs are saved under "doraemon_content/story{x}/LLM_json/1.json" ... a file for each image
    if args.image2json:

        print("Starting to convert images to json")
        # Read in prompt text
        with open(image2json_prompt, "r", encoding="utf-8") as file:
            prompt = file.read()

        # Loop through each image 
        for i in range(9,num_images+1):
            print(f"Calling LLM for image: {str(i)}.  Please wait...")
            response = askImageGPT(prompt, BASE_URL + "images/"+str(i)+".png", script_response_format,[])
            #print(response)
            response_json = json.loads(response)
            with open(BASE_URL+"LLM_json/"+str(i)+".json", "w", encoding="utf-8") as outfile:
                json.dump(response_json, outfile, ensure_ascii=False)
            
            print(f"Success:  Json file written to: {BASE_URL}LLM_json/{str(i)}.json")


    # -----------------> STEP 2: MANUAL REVIEW STEP <------------------
    # Go to folder "doraemon_content/story{x}/LLM_json/" and look at each json file
    # The LLM will often get the sequence of the script wrong.  
    # Sometimes the teacher will also have some opinion about which are the right vocab to select
    # if you want to add a vocab, with copilot installed, can just start typing and copilot can help
    # fill in the other fields.
    # Once completed, copy verified files over to "/final_json/" folder so it doesn't get 
    # accidentally overwritten.  The next step will be fetching from this folder.  

    # -----------------> STEP 3: AGGREGATE SCRIPT FILE <------------------
    # STEP 3: aggregate the json files in final_json into a single json file
    # This loops through all the json files, aggregates them into a single "aggregated_script.json" file
    # In addition, it places the title and subtitle key and values into the json object
    if args.aggregatejson:
        
        final_json = []
        for i in range(1,num_images+1):
            with open(BASE_URL+"final_json/"+str(i)+".json") as json_file:
                data = json.load(json_file)["script_list"]
                final_json += data
        with open(script_path, "w", encoding="utf-8") as outfile:
            json.dump({"script_list": final_json, "title": title, "subtitle": subtitle}, outfile, ensure_ascii=False)


    # -----------------> STEP 4: DATA FORMATTING <------------------
    # Manipulates the aggregated_script.json file and reformats them to be ready
    # To populate the fill-in-the-blank (FITB) exercise and also for chinese/english matching game
    # The jumbled sentences exercise also uses the FITB data file 
    if args.supportingjson:
        script2FITB_vocab_files(script_path, FITB_output_path, vocab_output_path)


    # -----------------> STEP 5: MANUAL REVIEW STEP <------------------
    # open up ...LLM_json/FITB_LLM.json file to do a quick review.  
    # for all sentences suitable for "jumbled sentence" exercise, add a key/value pair ' "seg": True '
    # after editing, move into "final_json" folder and save as "FITB_final.json"
    # likewise, after checking vocab_LLM.json, move into "final_json" folder and save as "vocab_final.json"


    # -----------------> STEP 6: GENERATE PPT DECK <------------------
    if args.createfinaldeck:
        print("Creating Lesson Powerpoint Deck....")
        img_path = BASE_URL+"images/"
        create_presentation(img_path, num_images, template_path, output_path, script_path, FITB_final_path, vocab_final_path)