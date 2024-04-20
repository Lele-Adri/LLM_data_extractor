
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from openai import OpenAI

GPT_4_MODEL = "gpt-4-1106-preview" 
GPT_3_MODEL = "gpt-3.5-turbo-1106" 


load_dotenv()

def get_chat_gpt_3() -> ChatOpenAI:
    return get_chat_gpt_model(GPT_3_MODEL, 10000, 0.1)

def get_chat_gpt_4() -> ChatOpenAI:
    return get_chat_gpt_model(GPT_4_MODEL, 10000, 0.1)

def get_gpt_3() -> OpenAI:
    return get_gpt_model(GPT_3_MODEL, 10000, 0.1)

def get_gpt_4() -> OpenAI:
    return get_gpt_model(GPT_4_MODEL, 10000, 0.1)


def get_gpt_model(model: str, max_tokens: int, temperature: float) -> ChatOpenAI:
    return ChatOpenAI(
        temperature=temperature,
        model=model,
        verbose=True,
        max_tokens=max_tokens,
        api_key=os.getenv("OPENAI_API_KEY")
    )

def get_chat_gpt_model(model: str, max_tokens: int, temperature: float) -> ChatOpenAI:
    return ChatOpenAI(
        temperature=temperature,
        model=model,
        verbose=True,
        max_tokens=max_tokens,
        api_key=os.getenv("OPENAI_API_KEY")
    )


async def get_gpt_3_completion(prompt):
    return get_completion(prompt, model=GPT_3_MODEL)

async def get_gpt_4_completion(prompt):
    return await get_completion(prompt, model=GPT_4_MODEL)

async def get_completion(prompt, model):
    messages = [{"role": "user", "content": prompt}]
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content



# def load_prompt_template(file_path):
#     with open(file_path, 'r') as file:
#         prompt_text = file.read()
#     return prompt_text