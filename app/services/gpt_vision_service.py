import base64, os, requests
from dotenv import load_dotenv

from app.app_constants import OPENAI_API_KEY_ENVIRONMENT_VARIABLE_NAME

load_dotenv()

# OpenAI API Key
api_key = os.getenv(OPENAI_API_KEY_ENVIRONMENT_VARIABLE_NAME)

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def get_content_with_Vision(image_path, info_type):

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    prompt_text = f"""You are given the screenshot of a webpage.
    Do not output your reasoning.
    Read carefully the screenshot and output any information related to:{info_type}.
    If there is no information related to {info_type}, output an empty string."""

    payload = {
    "model": "gpt-4-turbo",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt_text
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300,
    'temperature': 0
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return(response.json().get('choices')[0].get('message').get('content'))
