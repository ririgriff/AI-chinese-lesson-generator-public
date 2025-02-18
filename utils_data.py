import json


def script2FITB_vocab_files(script_path, FITB_output_path, vocab_output_path):
    with open(script_path) as json_file:
            data = json.load(json_file)["script_list"]
            FITB_sentences = []
            vocab_list = {}
            count = 1

            # Loop through each line of the script
            for line in data:

                # each line of script may have more than 1 vocab so need to loop through vocab
                for vocab in line["vocab"]:
                    # sentences that are too short are not suitable for fill-in-the-blank exercise - skip over
                    if len(line["script_text"]) > 15: 
                        FITB_sentences.append({
                            "count": count,
                            "sentence": line["script_text"].replace(vocab["SC_vocab"], "_________"),
                            "vocab": vocab["SC_vocab"],
                            "complete_sentence": line["script_text"]})
        
                        #vocab_list is a dictionary with the SC_vocab as the key rather than a list to remove duplicates
                        vocab_list.update({vocab["SC_vocab"]: {"SC_vocab": vocab["SC_vocab"], "TC_vocab": vocab["TC_vocab"], "english_meaning":vocab["english_meaning"]}})
                        count += 1
            with open(FITB_output_path, "w", encoding="utf-8") as outfile:
                json.dump({"FITB_questions": FITB_sentences}, outfile, ensure_ascii=False)

            with open(vocab_output_path, "w", encoding="utf-8") as outfile:
                json.dump({"vocab_list": vocab_list}, outfile, ensure_ascii=False)