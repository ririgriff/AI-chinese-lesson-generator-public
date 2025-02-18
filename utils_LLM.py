from openai import OpenAI  
import openai
import json
import os
from dotenv import load_dotenv
import base64

def get_openai_key():
    Openai_API_KEY = os.getenv('OPENAI_API_KEY')
    if Openai_API_KEY == None:
        load_dotenv()
        Openai_API_KEY = os.getenv('OPENAI_API_KEY')
    return Openai_API_KEY

def read_file_as_json(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
    
    try:
        data_json = json.loads(data)
        #print(data_json)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    return data_json

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")



def askGPT(prompt, response_format_file, chat_history):

    targetformat = read_file_as_json(response_format_file)

    #print("chat history inside utils_LLM: "+ str(len(chat_history))+": "+str(chat_history[0]))
    
    # GET KEY FROM ENVIRONMENT
    Openai_API_KEY = os.getenv('OPENAI_API_KEY')
    if Openai_API_KEY == None:
        load_dotenv()
        Openai_API_KEY = os.getenv('OPENAI_API_KEY')
    openai.api_key = Openai_API_KEY

    # ASSEMBLE MESSAGE_ARRAY
    chat_history.append({"role": "user", "content": prompt})

    completion = openai.chat.completions.create(
        model="o3-mini",
        messages= chat_history,
        response_format = targetformat
    )

    # Response Syntax:  https://platform.openai.com/docs/api-reference/chat/create
    print("completion: ", completion)
    #print("finish reason: ", completion.choices[0].finish_reason)
    response_content = completion.choices[0].message.content
    if response_content == None:
        print("LLM returned with no content")
    else:
        print("LLM returned with this result:" + response_content[:500]) 

    # Need to add a check that the response came back OK

    # with open('LLM_response.json', 'w') as file:
    #     file.write(response_content)

    # Append current response to chat history
    chat_history.append({"role":"assistant", "content": response_content})

    return (json.loads(response_content), chat_history)

    #return {"current_response": True, "chat_history": True} 

def askImageGPT(prompt, imagefile, response_format_file, chat_history):

# GET KEY FROM ENVIRONMENT
    targetformat = read_file_as_json(response_format_file)
    openai.api_key = get_openai_key()

    # ASSEMBLE MESSAGE_ARRAY
    chat_history.append({"role": "user", "content": prompt})

    # Getting the Base64 string
    base64_image = encode_image(imagefile)

    response = openai.chat.completions.create(
        model="o1",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        response_format = targetformat
    )

    return response.choices[0].message.content
