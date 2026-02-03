from ActionProcesser.ActionFunctions.BaseAction import ActionExecutedResponse, BaseAction, ParametersType, ParsedParameter
from typing import *

class SendWhatsappAction(BaseAction):
  def __init__(self):
    super().__init__()
    self.message: ParsedParameter = None
    self.contact_name: ParsedParameter = None
  
  def name(self) -> str:
    return "SEND_WHATSAPP"
  
  def description(self) -> str:
    return "Envia uma mensagem para um contato do usuário no whatsapp."
  
  def getParametersDescription(self) -> List[ParametersType]:
    return [
      {
        "name": "contact_name",
        "type": "string",
        "description": "O nome do contato, o usuário deve passar esse nome corretamente."
      },
      {
        "name": "message",
        "type": "string",
        "description": "A mensagem a ser enviada, deixe-a o mais natural possível."
      }
    ]
  
  def setParameters(self, parameters: dict) -> None:
    self.message: ParsedParameter = self.parseParameter("message", parameters)
    self.contact_name: ParsedParameter = self.parseParameter("contact_name", parameters)
  
  def __checkParameters(self, parameters: dict) -> bool:
    self.parseParameter("message", parameters)
    self.parseParameter("contact_name", parameters)
    return True
  
  def checkActionObject(self, actionObject: dict) -> bool:
    try:
      return actionObject.get("name") == self.name() and self.__checkParameters(actionObject.get("parameters", {}))
    except ValueError:
      return False
  
  
  #---------------------EXECUTION---------------------#
  
  def execute(self) -> ActionExecutedResponse:
    return ActionExecutedResponse(
      hasResponse=True,
      responseText=f"Mensagem enviada para {self.contact_name} no WhatsApp: {self.message}"
    )