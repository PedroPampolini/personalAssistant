# import abstract class
from abc import ABC, abstractmethod
from typing import *

class ParametersType(TypedDict):
  name: str
  type: str
  description: str
  
class ParsedParameter(TypedDict):
  name: str
  type: str
  value: Any
  
  
class ActionExecutedResponse(TypedDict):
  hasResponse: bool
  responseText: str
  

class BaseAction(ABC):
  
  @abstractmethod
  def getParametersDescription(self) -> List[ParametersType]:
    pass
  
  @abstractmethod
  def name(self) -> str:
    pass
  
  @abstractmethod
  def description(self) -> str:
    pass
  
  @abstractmethod
  def setParameters(self, parameters: dict) -> None:
    pass
  
  @abstractmethod
  def checkActionObject(self, actionObject: dict) -> bool:
    pass
  
  def validateParameter(self, parameter: Dict) -> bool:
    type = parameter.get("type", "")
    value = parameter.get("value", None)
    if type == "string":
      return isinstance(value, str)
    elif type == "integer":
      return isinstance(value, int)
    elif type == "float":
      return isinstance(value, float)
    elif type == "boolean":
      return isinstance(value, bool)
    elif type == "list":
      return isinstance(value, list)
    elif type == "dict":
      return isinstance(value, dict)
    return False
  
  def parseParameter(self, parameterName, parameter: Dict) -> ParsedParameter:
    parameter = parameter.get(parameterName, None)
    if parameter is None:
      raise ValueError(f"Parameter '{parameterName}' not found")
    parameterType = parameter.get("type", None)
    parameterValue = parameter.get("value", None)
    if not (parameterType and parameterValue):
      raise ValueError(f"Parameter '{parameterName}' is missing type or value")
    if not self.validateParameter(parameter):
      raise TypeError(f"Parameter '{parameterName}' has invalid type or value")
    return ParsedParameter(
      name=parameterName,
      type=parameterType,
      value=parameterValue
    )
  
  @abstractmethod
  def execute(self) -> ActionExecutedResponse:
    pass
  
 