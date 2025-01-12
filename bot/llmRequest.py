from g4f.client import Client

model = "gpt-4o"
client = Client()

def sendRequest(data: str) -> str:
  response = client.chat.completions.create(messages=data, model=model, web_search=True)
  return response.choices[0].message.content