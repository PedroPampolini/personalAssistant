import time
import env
import os
from typing import *
from contants import *
from globals import assistant
from utils import debug
from bot.bot import Bot
import speech_recognition as sr
from colorama import Fore, Style

def checkFolders():
  if not os.path.exists(env.TMP_FOLDER_PATH):
    os.makedirs(env.TMP_FOLDER_PATH)

def getAudio():
  r  = sr.Recognizer()
  with sr.Microphone(device_index=0) as source:
    debug('Say Something')
    audio = r.listen(source)
  data = ''
  try:
    # recognition in portuguese
    data = r.recognize_google(audio, language=env.LANGUAGE)
  except sr.UnknownValueError:
    debug('We cannot understand the audio, unknown error')
  except sr.RequestError as e:
    debug('Service Error ' + e)

  return data

def getUserInput() -> Tuple[str, bool]:
  if env.INTERACTION_TYPE == InteractionType.AUDIO:
    data: str = getAudio()
    if env.BOT_NAME in data.lower():
      return data, True
    return data, False
  else:
    data = input(Fore.BLUE + 'You: ' + Style.RESET_ALL)
    return data, True

def displayResponse(response: str, assistant: Bot):
  if not response:
    return
  if env.INTERACTION_TYPE == InteractionType.AUDIO:
    assistant.say(response)
  else:
    print(Fore.YELLOW + 'Bot: ' + Style.RESET_ALL + response)

def run():
  print('Bot Iniciado')
  while True:
    try:
      data, isTriggered = getUserInput()
      if isTriggered:
        response = assistant.getResponse(data)
        displayResponse(response, assistant)
      else:
        debug('Não Disparado: ' + data)
      time.sleep(0.1)
    except Exception as e:
      print(f'Erro: {e}')


if __name__ == '__main__':
  checkFolders()
  run()