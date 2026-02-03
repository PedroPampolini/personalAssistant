from MiddleWare.middleware import Middleware

while True:
  userInput = input("You: ")
  response = Middleware.sendToBot(userInput)
  print("Assistant:", response)