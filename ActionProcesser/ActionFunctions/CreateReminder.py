from ActionProcesser.ActionFunctions.BaseAction import ActionExecutedResponse, BaseAction, ParametersType, ParsedParameter
from datetime import datetime, timedelta
from typing import *
import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class GoogleAgendaService:
  def __init__(self):
    self.__google_calendar_scopes = ["https://www.googleapis.com/auth/calendar"]
    self.__credentials = None
    token_path = os.path.join(os.path.dirname(__file__), "..", "..", "credentials", "google-api-token.json")
    creds_path = os.path.join(os.path.dirname(__file__), "..", "..", "credentials", "google-api-credentials.json")
    
    # debug remover dps
    if(not os.path.exists(token_path)):
      print("aaaaaa nao achou o path do token", token_path)
    if(not os.path.exists(creds_path)):
      print("aaaaaa nao achou o path das credenciais", creds_path)
      
    if(os.path.exists(token_path)):
      self.__credentials = Credentials.from_authorized_user_file(token_path, self.__google_calendar_scopes)
    if(not self.__credentials or not self.__credentials.valid):
      flow = InstalledAppFlow.from_client_secrets_file(creds_path, self.__google_calendar_scopes)
      self.__credentials = flow.run_local_server(port=0)
      with open(token_path, "w") as token:
        token.write(self.__credentials.to_json())
    self.__service = build("calendar", "v3", credentials=self.__credentials)
    
    
  def getService(self):
    return self.__service
  
googleAgendaServiceInstance = GoogleAgendaService()

class CreateReminderAction(BaseAction):
  def __init__(self):
    super().__init__()
    self.title: ParsedParameter = None
    self.descriptionValue: ParsedParameter = None
    self.initTime: ParsedParameter = None
    self.finalTime: ParsedParameter = None

  
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
        "name": "initTime",
        "type": "string",
        "description": "O horário inicial do lembrete no formato \"YYYY-MM-DD HH:MM\"."
      },
      {
        "name": "finalTime",
        "type": "string",
        "description": "O horário final do lembrete no formato \"YYYY-MM-DD HH:MM\"."
      },
    ]
  
  def setParameters(self, parameters: dict) -> None:
    self.title: ParsedParameter = self.parseParameter("title", parameters)
    self.descriptionValue: ParsedParameter = self.parseParameter("description", parameters)
    self.initTime: ParsedParameter = self.parseParameter("initTime", parameters)
    self.finalTime: ParsedParameter = self.parseParameter("finalTime", parameters)
  
  def __validateTime(self, timeStr: str) -> bool:
    try:
      datetime.strptime(timeStr, "%Y-%m-%d %H:%M")
      return True
    except ValueError:
      return False
  
  def __checkParameters(self, parameters: dict) -> bool:
    self.parseParameter("title", parameters)
    self.parseParameter("description", parameters)
    initTime: ParsedParameter = self.parseParameter("initTime", parameters)
    finalTime: ParsedParameter = self.parseParameter("finalTime", parameters)
    return self.__validateTime(initTime.get("value", "")) and self.__validateTime(finalTime.get("value", ""))
  
  def checkActionObject(self, actionObject: dict) -> bool:
    try:
      return actionObject.get("name") == self.name() and self.__checkParameters(actionObject.get("parameters", {}))
    except ValueError:
      return False
  
  
  #---------------------EXECUTION---------------------#
  
  

  def buildEventBody(self) -> dict:
    event = {
      "summary": self.title.get("value"),
      "description": self.descriptionValue.get("value"),
      "start": {
        "dateTime": datetime.strptime(self.initTime.get("value"), "%Y-%m-%d %H:%M").isoformat(),
        "timeZone": "America/Sao_Paulo",
      },
      "end": {
        "dateTime": datetime.strptime(self.finalTime.get("value"), "%Y-%m-%d %H:%M").isoformat(),
        "timeZone": "America/Sao_Paulo",
      },
    }
    return event
  
  
  def execute(self) -> ActionExecutedResponse:
    print(f"Lembrete criado: {self.title} - {self.descriptionValue} às {self.initTime} até {self.finalTime}")
    
    createEvent = googleAgendaServiceInstance.getService().events().insert(
      calendarId="primary",
      body=self.buildEventBody()
    ).execute()
    
    print("Evento criado: %s" % (createEvent.get("htmlLink")))
    
    return ActionExecutedResponse(
      hasResponse=True,
      responseText=f"Lembrete criado: {self.title} - {self.descriptionValue} às {self.initTime} até {self.finalTime}"
    )