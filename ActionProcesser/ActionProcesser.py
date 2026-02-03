from Constants.MessagesPlaceholders import ACTIONS_FORMATED_LIST_PLACEHOLDER, CONTEXT_FORMATED_LIST_PLACEHOLDER, USER_MEMORY_TOKEN
from chatHistoryController.chatController import ChatHistoryController
from Memoryzer.memorizer import memoryzerInstance
from ActionProcesser.ActionFunctions.BaseAction import BaseAction
from ActionProcesser.ActionFunctions.AllAction import buildActionsText, ALL_FUNCTIONS_MAP
from ContextBuilder.ContextBuilder import contextBuilderInstance
import json

PRE_PROMPT = '''Você é um processador de ações. Seu objetivo é analisar a mensagem do usuário e determinar a ação apropriada a ser executada. Responda apenas com um objeto JSON que descreva a ação a ser tomada, seguindo esta estrutura:
{
  "name": "nome_da_ação",
  "parameters": {
    "parametro1": {
      "type": "tipo_do_parametro1",
      "value": "valor_do_parametro1",
    },
    "parametro2": {
      "type": "tipo_do_parametro2",
      "value": "valor_do_parametro2",
    }
  }
}
As ações disponíveis são:
{{ACTIONS-FORMATED-LIST}}
Certifique-se de que o JSON retornado seja bem formatado e válido. Não inclua explicações ou texto adicional fora do objeto JSON.
Você pode utilizar a memória do ActionProcessor para auxiliar à criar os valores dos parâmetros das ações. Sendo a memória as seguintes informações:
{{USER-MEMORY-FORMATED-LIST}}
Você também pode utilizar informações de contexto para ajudar a determinar a ação correta e os valores dos parâmetros dessa ação, o contexto é o seguinte:
{{CONTEXT-FORMATED-LIST}}
'''

# TODO: Fazer um historico de ações realizadas e enviar um historico de até 5 (avaliar esse numero melhor) mensagens para ele saber melhor como processar
# ^^ Essa ação pode ficar muito complexa, então pode ser que nao de certo, avaliar posteriormente

class ActionProcesser:
  def __init__(self):
    self.chatController = ChatHistoryController()
  
  def __buildPreprompt(self) -> str:
    preprompt = PRE_PROMPT
    actionsText = buildActionsText()
    preprompt = preprompt.replace(ACTIONS_FORMATED_LIST_PLACEHOLDER, actionsText)
    userMemory = memoryzerInstance.getUserMemoryFormatedList()
    preprompt = preprompt.replace(USER_MEMORY_TOKEN, userMemory)
    contextText = contextBuilderInstance.getContextText()
    preprompt = preprompt.replace(CONTEXT_FORMATED_LIST_PLACEHOLDER, contextText)
    return preprompt   
  
  def createPrePromptedMessage(self, message: str) -> str:
    self.chatController.clearChatHistory()
    self.chatController.addSystemMessage(self.__buildPreprompt())
    self.chatController.addUserMessage(message)
    response = self.chatController.getResponse()
    return response[-1]["content"]
  
  def processAction(self, userMessage: str) -> dict:
    maxTries = 3
    for attempt in range(maxTries):
      try:
        actionString = self.createPrePromptedMessage(userMessage)
        action = self.getAction(actionString)
        response = action.execute()
        if response.get("hasResponse", False):
          return response.get("responseText", "")
        return ""
      except (ValueError, TypeError) as e:
        print(f"Erro ao processar ação: {str(e)} - Tentativa {attempt + 1} de {maxTries}")
  
  def getAction(self, actionString: str) -> BaseAction:
    validatedAction = None
    try:
      self.__validateActionObject(actionString)
      validatedAction = json.loads(actionString)
    except (ValueError, TypeError) as e:
      raise e
    
    action: BaseAction = ALL_FUNCTIONS_MAP.get(validatedAction.get("name"), None)
    if action is None:
      raise ValueError(f"Action '{validatedAction.get('name')}' not found")
    
    action.setParameters(validatedAction.get("parameters", {}))
    if not action.checkActionObject(validatedAction):
      raise ValueError(f"Action parameters are invalid for action '{validatedAction.get('name')}': {validatedAction.get('parameters', {})}")
    
    return action
    
  def __validateActionObject(self, response: str) -> bool:
    actionObject = None
    try:
      actionObject = json.loads(response)
    except json.JSONDecodeError:
      raise ValueError("Invalid JSON format")
    
    if(self.__checkActionObjectStructure(actionObject)):
      return actionObject
    
    return {} # will never reach here because of the raises in __checkActionObjectStructure
    
  def __checkActionObjectStructure(self, actionObject: dict) -> bool:
    requiredKeys = {"name", "parameters"}
    if not all(key in actionObject for key in requiredKeys):
      raise ValueError("Missing required keys in action object")
    if not isinstance(actionObject["name"], str):
      raise TypeError("The 'name' field must be a string")
    if not isinstance(actionObject["parameters"], dict):
      raise TypeError("The 'parameters' field must be a dictionary")
    return True
  
actionProcesserInstance = ActionProcesser()