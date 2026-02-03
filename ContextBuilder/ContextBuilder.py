from typing import *
from datetime import datetime


class ContextBuilder:
  def __init__(self):
    pass
  
  def __buildContextText(self) -> str:
    contextObject = {
      "currentTime": datetime.now().strftime("%H:%M:%S"),
      "todayDate": datetime.now().strftime("%d/%m/%Y")
    }
    
    contextText = "Contexto atual:\n"
    for key, value in contextObject.items():
      contextText += f'- "{key}": {value}\n'
    return contextText
  
  def getContextText(self) -> str:
    return self.__buildContextText()
  
contextBuilderInstance = ContextBuilder()