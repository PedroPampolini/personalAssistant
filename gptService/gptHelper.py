from g4f.client import  Client
from typing import *
from gptService.gptTypes import *
from g4f import providers

from g4f.client import ClientFactory



GPT_MODEL = "openai"  # You can change this to any other model supported by g4f
GEMINI_MODEL="models/gemini-flash-lite-latest"

def getResponse(chat: GptChatHistory, webSearch:bool = False) -> str:
  client: Client = ClientFactory.create_client("gemini")
  # print("Using pollinations client")
  # client = Client()
  response = client.chat.completions.create(
    model=GEMINI_MODEL,
    messages=chat,
    web_search=webSearch,
  )
  return response.choices[0].message.content