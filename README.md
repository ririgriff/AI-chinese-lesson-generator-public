# AI-chinese-lesson-generator

This repository contains code that ingests a number of PNG images of a comic book story and
turns it into a Chinese Lesson with workbook exercises in powerpoint format with "teacher-in-the-loop".

With this code, you can create outputs like this: [sample lesson deck](output_lesson/PDF/lesson2_2025-02-17_FINAL.pdf)

Disclaimer: this is a project for personal educational use. Please make sure you
have the rights to use whatever images you plan to ingest with this code.

# Setting up

After cloning the repository, you need to:

### set up virtual environment

- Open Terminal, navigate to project directory and run this command to ensure the packages you install are isolated from the rest of your computer system. Below are the commands for macOS/Linux.

```
python -m venv venv
source venv/bin/activate
```

to get out of the virtual environment after you are done with project, type:

```
deactivate
```

-

### Install Libraries

- Open Terminal, navigate to project directory and run this command to install the required libraries

```
pip install -r requirements.txt
```

### Set up API keys

- set up your environment variables to pass in your OpenAI key. To see how the code retreives the API key, look at [utils_LLM.py](utils_LLM.py) (get_openai_key function). To run the code locally, you can create and place your API keys in an ".env" file in the root directory. The code will fetch from here if it cannot fetch any valid environment variables.

- follow the step by step instructions in [main.py](main.py). Below is an overview of the steps. some manual steps are involved to give the educator more control over what goes into the final deck.

---

# Running the Code

### Step 0 (optional)

```
python main.py --createindexdeck
```

To take the [powerpoint template](powerpoint_template/doraemon_lesson_template_v1.pptx) and populate all the placeholders with index numbers to facilitate the coding of the utils_genslides functions. Don't need to do this if powerpoint template has not changed.

See examples of results here: [template_with_index.pptx](powerpoint_template/template_with_index.pptx)

---

### STEP 1: Convert Images to JSON files

```
python main.py --image2json
```

This step takes all the images you have provided, one by one, and converts each into a json format with key vocab extracted using OpenAI o1 model. Please note that o1 is the _most expensive model_ that OpenAI has at the moment - so watch the costs! But o3-mini cannot support images at the time I'm coding this and GPT-4o is unable to do this task well.

At this point, you should also adjust the "configuration variables" inside main.py to reflect the correct details for the lesson you are generating.

See examples of results here: [json output folder](doraemon_content/story1/LLM_json/)

---

### STEP 2: TEACHER-IN-THE-LOOP

Check all the files from step 2 manually. Once approved, copy into LLM_final folder
See examples of results here: [post-review json files for ingestion](doraemon_content/story1/LLM_final/)

---

### STEP 3: Concatenate all the json files into a single "Aggregated script" file

```
python main.py --aggregatejson
```

See examples of results here: [aggregrated_script json file](doraemon_content/story1/final_json/aggregate_script.json)

---

### STEP 4: Reformats "Aggregated Script" file into 2 additional json files

```
python main.py --supportingjson
```

- See examples of file 1 here: [fill-in-the-blank data file](doraemon_content/story1/LLM_json/LLM_FITB.json)
- See examples of file 2 here: [list of vocab data file](doraemon_content/story1/LLM_json/LLM_vocab.json)

---

### STEP 5: TEACHER-IN-THE-LOOP Manual check

check the two files from step 4. When done, save to final_json folder under the correct filenames. Read main.py for details

---

### STEP 6: Create the powerpoint deck

```
python main.py --createfinaldeck
```

Voila! Find your deck in "output_lesson/" folder [output powerpoint deck](output_lesson/)

---

# Some explanation to what's going on under the hood

### The key inputs to the code include:

- PNG images of the comic story (1.png ... 12.png)
- prompt text that goes into the LLM request
- json schema that goes into the LLM request defining the output format of the LLM
- powerpoint template file

---

### Intermediary outputs:

- 1.json... 12.json --> one file for each input image
- aggregated_script.json --> assembles all of the files into one after human review
- FITB_LLM.json --> formats aggregated_script into a format suitable for 2 of the 3 workbook exercises
- vocab_LLM.json --> formats aggregrated_script into a format suitable 1 of the workbook exercises

---

### Final inputs into PPT deck production

- aggregated_script.json
- FITB_final.json --> this is the post-human-review version of the FITB_LLM file
- vocab_final.json --> this is the post-human-review version of the vocab_LLM file

---

### Powerpoint Output

- decks are stored inside "output_lesson" folder
