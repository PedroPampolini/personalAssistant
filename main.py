from MiddleWare.middleware import Middleware
from VoiceConverter.VoiceConverter import voiceConverterInstance

isVoicedOutput = True

while True:
  userInput = input("You: ")
  response: str = Middleware.sendToBot(userInput)
  if(isVoicedOutput):
    voiceConverterInstance.Text2Speech(response)
  else:
    print("Assistant:", response)