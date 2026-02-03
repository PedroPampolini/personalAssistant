from ActionProcesser.ActionFunctions.BaseAction import ActionExecutedResponse, BaseAction, ParametersType, ParsedParameter
from typing import *

class SearchWebAction(BaseAction):
  def __init__(self):
    super().__init__()
    self.query: ParsedParameter = None
  
  def name(self) -> str:
    return "SEARCH_WEB"
  
  def description(self) -> str:
    return "Realiza uma busca na web."
  
  def getParametersDescription(self) -> List[ParametersType]:
    return [
      {
        "name": "query",
        "type": "string",
        "description": "A consulta de busca."
      }
    ]
  
  def setParameters(self, parameters: dict) -> None:
    self.query: ParsedParameter = self.parseParameter("query", parameters)
  
  def checkActionObject(self, actionObject: dict) -> bool:
    try:
      return actionObject.get("name") == self.name() and self.parseParameter("query", actionObject.get("parameters", {}))
    except ValueError:
      return False
  
  #---------------------EXECUTION---------------------#
  
  def execute(self) -> ActionExecutedResponse:
    print(f"Realizando busca na web para a consulta: {self.query}")
    # Aqui você implementaria a lógica real de busca na web.
    return ActionExecutedResponse(
      hasResponse=True,
      responseText=f"Resultados da busca para a consulta: {self.query}"
    )