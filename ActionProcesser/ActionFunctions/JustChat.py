from Constants.MessagesPlaceholders import CONTEXT_FORMATED_LIST_PLACEHOLDER, USER_MEMORY_TOKEN
from ActionProcesser.ActionFunctions.BaseAction import ActionExecutedResponse, BaseAction, ParametersType, ParsedParameter
from chatHistoryController.chatController import ChatHistoryController
from Memoryzer.memorizer import memoryzerInstance
from ContextBuilder.ContextBuilder import contextBuilderInstance
from typing import *

JUST_CHAT_PRE_PROMPT = '''Vocé é um assistente virtual, deve responder e ser útil ao usuário. Para auxiliar nas respostas, será fornecido algumas informações úteis à você.
Primeiramente irá receber algumas informações úteis de memórias do usuário, sendo elas:
{{USER-MEMORY-FORMATED-LIST}}
Além disso, você também receberá um contexto adicional que pode ser útil para responder ao usuário, sendo o seguinte:
{{CONTEXT-FORMATED-LIST}}
Você pode usar essas informações apenas caso seja necessário para responder às mensagens do usuário. Caso não seja necessário, apenas responda normalmente.
As suas respostas deve ser apenas texto puro, sem usar formatação markdown, HTML, ou qualquer outro tipo de caractere especial. Responda apenas texto puro, como se estivesse em uma conversa normal.

Utilize pontuações na sua resposta textual na forma que elas tenham efeito no Text-To-Speech (TTS). Seu texto será convertido em fala, então utilize vírgulas, pontos, interrogações, exclamações, reticências, etc., para que a fala fique mais natural. Utilize também táticas como "onomatopéias" para tornar a fala mais natural possível.
'''

class JustChatAction(BaseAction):
  def __init__(self):
    super().__init__()
    self.chatHistory: ChatHistoryController = ChatHistoryController()
    self.message: ParsedParameter = None
    
    self.chatHistory.addSystemMessage(self.__buildPreprompt())
  
  def __buildPreprompt(self) -> str:
    preprompt = JUST_CHAT_PRE_PROMPT
    userMemory = memoryzerInstance.getUserMemoryFormatedList()
    preprompt = preprompt.replace(USER_MEMORY_TOKEN, userMemory)
    contextText = contextBuilderInstance.getContextText()
    preprompt = preprompt.replace(CONTEXT_FORMATED_LIST_PLACEHOLDER, contextText)
    return preprompt
  
  def name(self) -> str:
    return "JUST_CHAT"
  
  def description(self) -> str:
    return "Apenas responda à mensagem do usuário sem executar nenhuma ação."
  
  def getParametersDescription(self) -> List[ParametersType]:
    return [
      {
        "name": "message",
        "type": "string",
        "description": "A mensagem que o usuário enviou. Deve ser EXATAMENTE a mesma mensagem que o usuário enviou que foi analisada pelo ActionProcessor."
      }
    ]
  
  def setParameters(self, parameters: dict) -> None:
    self.message: ParsedParameter = self.parseParameter("message", parameters)
  
  def checkActionObject(self, actionObject: dict) -> bool:
    try:
      return actionObject.get("name") == self.name() and self.parseParameter("message", actionObject.get("parameters", {}))
    except ValueError:
      return False
  
  
  #---------------------EXECUTION---------------------#
  
  def sendMessage(self, message: str) -> str:
    self.chatHistory.addUserMessage(message)
    response = self.chatHistory.getResponse()[-1]["content"]
    return response
  
  def execute(self) -> ActionExecutedResponse:
    text = self.message.get("value", "")
    response = self.sendMessage(text)
    return ActionExecutedResponse(
      hasResponse=True,
      responseText=response
    )