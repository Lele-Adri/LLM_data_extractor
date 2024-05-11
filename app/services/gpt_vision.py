import base64, os, requests
from dotenv import load_dotenv

load_dotenv()

# OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "./standard_screenshot.png"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

prompt_text = """Check if there is a cookie banner on the image.
You are asked to output a string:

    * If there is no cookie banner, output an empty string.

    *If there is a cookie banner on the image, output a string \
containing the button that I have to click to accept cookies."""

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

print(response.json().get('choices')[0].get('message').get('content'))
