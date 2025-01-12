from typing import *
import re
import os
from bot import tts
import env
import json
from momentContext.index import allMomentContexts
from gtts import gTTS
from actions.index import allActions
from g4f.client import Client
from utils import debug
from bot import llmRequest

class Bot:
  def __init__(self):
    self.prePrompt = open(env.PREPROMPT_FILE_PATH, 'r', encoding='utf-8').read()
    self.history = [{'role': 'system', 'content': self._buildPrePrompt()}]
    self.memory = json.loads(open(env.MEMORY_FILE_PATH, 'r', encoding='utf-8').read())
    self.promptWithoutPrePrompt = 0

  def _buildChat(self, prompt: str) -> List[Dict[str, str]]:
    if self._needPrePrompt():
      debug('Re adding pre prompt')
      prompt = self._buildPrePrompt() + prompt
    return self.history + [{'role': 'user', 'content': prompt}]

  def _buildMomentContext(self):
    contextText = ''
    for context in allMomentContexts:
      contextText += context

    return contextText
  
  def _buildMemoryContext(self):
    memory = json.loads(open(env.MEMORY_FILE_PATH, 'r', encoding='utf-8').read())
    self.memory = memory
    debug('Memory:', self.memory)
    memoryText = ''
    for key in memory:
      memoryText += f'- {key}: {memory[key]}\n'

    return memoryText

  def _buildActionsList(self):
    actionsText = ''
    for action in allActions.values():
      actionsText += f'- {action.keyword}: {action.description}\n'
    return actionsText

  def _buildPrePrompt(self):
    preprompt = open(env.PREPROMPT_FILE_PATH, 'r', encoding='utf-8').read()
    momentContext = self._buildMomentContext()
    memoryContext = self._buildMemoryContext()
    preprompt = preprompt.replace(env.MOMENT_CONTEXT_PLACEHOLDER, momentContext)
    preprompt = preprompt.replace(env.MEMORY_CONTEXT_PLACEHOLDER, memoryContext)
    preprompt = preprompt.replace(env.ACTIONS_PLACEHOLDER, self._buildActionsList())
    preprompt = preprompt.replace(env.BOT_NAME_PLACEHOLDER, env.BOT_NAME)
    return preprompt

  def _checkResponse(self, response):
    regex = r'^\{"message":\s*".*?",\s*"action":\s*".*?",\s*"memory":\s*\{(?:\s*".*?":\s*".*?"(?:,\s*".*?":\s*".*?")*)?\s*\}\}$'
    if not re.match(regex, response):
      return False
    return True

  def _needPrePrompt(self) -> bool:
    if self.promptWithoutPrePrompt >= 3:
      self.promptWithoutPrePrompt = 0
      return True
    self.promptWithoutPrePrompt += 1
    return False

  def sendRequest(self, data: str) -> str:
    chat = self._buildChat(data)
    self.history = chat
    return llmRequest.sendRequest(chat)

  def saveHistory(self):
    filePath = os.path.join(env.TMP_FOLDER_PATH, 'history.json')
    with open(filePath, 'w', encoding='utf-8') as file:
      file.write(json.dumps(self.history, indent=2))

  def getResponse(self, data: str) -> str:
    response = self.sendRequest(data)
    maxTries = 3
    for i in range(maxTries):
      if self._checkResponse(response):
        break
      response = self.sendRequest(data)
      debug(f'Retrying... {i+1}/{maxTries}')
    debug('Response:', response)
    if not self._checkResponse(response):
      self.history = self.history[:-1]
      return "Desculpe, não entendi o que você disse."
    
    self.history += [{'role': 'assistant', 'content': response}]
    data = json.loads(response)
    actions = data['action']
    memory = data['memory']
    message = data['message']

    self._updateMemory(memory)

    try:
      willRespond = self.dispatchActions(actions)
    except Exception as e:
      debug(f'Erro ao executar ação: {e}')
      willRespond = True
    self.saveHistory()
    if not willRespond:
      return ''
    return message
  
  def _updateMemory(self, memory: Dict[str, str]):
    updatingMemory = False
    for key in memory:
      if key not in self.memory or self.memory[key] != memory[key]:
        updatingMemory = True
      self.memory[key] = memory[key]
    self.memory = dict(sorted(self.memory.items()))
    if updatingMemory:
      self._saveMemory()

  def _saveMemory(self):
    with open(env.MEMORY_FILE_PATH, 'w', encoding='utf-8') as file:
      file.write(json.dumps(self.memory, indent=2))

  def triggerAction(self, action: str, *args):
    debug(f'Triggerring action: {action} - {args}')
    try:
      if args:
        allActions[action].connectArgs(args)
      return allActions[action]()
    except Exception as e:
      print(f'Erro ao executar ação {action}:\n{e}')
      

  def dispatchActions(self, action: str):
    actions = action.split(';')
    willResponde = True
    for action in actions:
      if not action:
        continue
      action, args = action.split(',', 1) if ',' in action else (action, '')
      args = args.split('&')
      args = [arg for arg in args if arg]
      willResponde = willResponde and self.triggerAction(action, *args) 
    return willResponde
  def say(self, data: str):
    tts.say(data)
