from ActionProcesser.ActionFunctions.BaseAction import ActionExecutedResponse, BaseAction, ParametersType, ParsedParameter
from datetime import datetime
from typing import *

class CreateReminderAction(BaseAction):
  def __init__(self):
    super().__init__()
    self.title: ParsedParameter = None
    self.descriptionValue: ParsedParameter = None
    self.time: ParsedParameter = None
  
  def name(self) -> str:
    return "CREATE_REMINDER"
  
  def description(self) -> str:
    return "Cria um lembrete para o usuário. "
  
  def getParametersDescription(self) -> List[ParametersType]:
    return [
      {
        "name": "title",
        "type": "string",
        "description": "O título do lembrete."
      },
      {
        "name": "description",
        "type": "string",
        "description": "A descrição do lembrete."
      },
      {
        "name": "time",
        "type": "string",
        "description": "O horário do lembrete no formato \"YYYY-MM-DD HH:MM\"."
      }
    ]
  
  def setParameters(self, parameters: dict) -> None:
    self.title: ParsedParameter = self.parseParameter("title", parameters)
    self.descriptionValue: ParsedParameter = self.parseParameter("description", parameters)
    self.time: ParsedParameter = self.parseParameter("time", parameters)
  
  def __validateTime(self, timeStr: str) -> bool:
    try:
      datetime.strptime(timeStr, "%Y-%m-%d %H:%M")
      return True
    except ValueError:
      return False
  
  def __checkParameters(self, parameters: dict) -> bool:
    self.parseParameter("title", parameters)
    self.parseParameter("description", parameters)
    time: ParsedParameter = self.parseParameter("time", parameters)
    return self.__validateTime(time.get("value", ""))
  
  def checkActionObject(self, actionObject: dict) -> bool:
    try:
      return actionObject.get("name") == self.name() and self.__checkParameters(actionObject.get("parameters", {}))
    except ValueError:
      return False
  
  
  #---------------------EXECUTION---------------------#
  
  def execute(self) -> ActionExecutedResponse:
    print(f"Lembrete criado: {self.title} - {self.descriptionValue} às {self.time}")
    return ActionExecutedResponse(
      hasResponse=True,
      responseText=f"Lembrete criado: {self.title} - {self.descriptionValue} às {self.time}"
    )