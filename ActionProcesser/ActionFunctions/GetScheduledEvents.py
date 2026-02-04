from ActionProcesser.ActionFunctions.BaseAction import ActionExecutedResponse, BaseAction, ParametersType, ParsedParameter
from datetime import datetime, timedelta, timezone
from typing import *
import json

from ActionProcesser.ActionFunctions.CreateReminder import googleAgendaServiceInstance
from chatHistoryController.chatController import ChatHistoryController

class GetScheduledEventsAction(BaseAction):
  def __init__(self):
    super().__init__()
    self.initTime: ParsedParameter = None
    self.finalTime: ParsedParameter = None

  
  def name(self) -> str:
    return "GET_SCHEDULED_EVENTS"
  
  def description(self) -> str:
    return "Retorna os eventos agendados no Google Agenda de um determinado período de tempo."
  
  def getParametersDescription(self) -> List[ParametersType]:
    return [
      {
        "name": "initTime",
        "type": "string",
        "description": "O horário inicial da busca dos eventos no formato \"YYYY-MM-DD HH:MM\"."
      },
      {
        "name": "finalTime",
        "type": "string",
        "description": "O horário final da busca dos eventos no formato \"YYYY-MM-DD HH:MM\"."
      },
    ]
  
  def setParameters(self, parameters: dict) -> None:
    self.initTime: ParsedParameter = self.parseParameter("initTime", parameters)
    self.finalTime: ParsedParameter = self.parseParameter("finalTime", parameters)
  
  def __validateTime(self, timeStr: str) -> bool:
    try:
      datetime.strptime(timeStr, "%Y-%m-%d %H:%M")
      return True
    except ValueError:
      return False
  
  def __checkParameters(self, parameters: dict) -> bool:
    initTime: ParsedParameter = self.parseParameter("initTime", parameters)
    finalTime: ParsedParameter = self.parseParameter("finalTime", parameters)
    return self.__validateTime(initTime.get("value", "")) and self.__validateTime(finalTime.get("value", ""))
  
  def checkActionObject(self, actionObject: dict) -> bool:
    try:
      return actionObject.get("name") == self.name() and self.__checkParameters(actionObject.get("parameters", {}))
    except ValueError:
      return False
  
  
  #---------------------EXECUTION---------------------# 
  
  def execute(self) -> ActionExecutedResponse:
    initPeriod = datetime.strptime(self.initTime.get("value"), "%Y-%m-%d %H:%M")
    initPeriod = datetime(
      initPeriod.year,
      initPeriod.month,
      initPeriod.day,
      initPeriod.hour,
      initPeriod.minute,
      tzinfo=timezone.utc
    ).isoformat()
    
    finalPeriod = datetime.strptime(self.finalTime.get("value"), "%Y-%m-%d %H:%M")
    finalPeriod = datetime(
      finalPeriod.year,
      finalPeriod.month,
      finalPeriod.day,
      finalPeriod.hour,
      finalPeriod.minute,
      tzinfo=timezone.utc
    ).isoformat()
    
    events = []
    pageToken = None
    
    print(f"Buscando eventos entre {initPeriod} e {finalPeriod}...")
    
    while True:
      eventsResult = googleAgendaServiceInstance.getService().events().list(
        calendarId="primary",
        timeMin=initPeriod,
        timeMax=finalPeriod,
        pageToken=pageToken
      ).execute()
      
      events.extend(eventsResult.get("items", []))
      pageToken = eventsResult.get("nextPageToken")
      if not pageToken:
        break

    print(f"Eventos encontrados: {len(events)}")
    eventsFilteredAttributes = [
      {
        "title": event.get("summary", "Sem título"),
        "description": event.get("description", ""),
        "start": event["start"].get("dateTime", event["start"].get("date")),
        "end": event["end"].get("dateTime", event["end"].get("date")),
      }
      for event in events]
    
    # ordenar eventos por data de início
    eventsFilteredAttributes.sort(key=lambda x: datetime.fromisoformat(x["start"].replace("Z", "+00:00")))
    print("Eventos filtrados e ordenados:")
    for event in eventsFilteredAttributes:
      print(event)
    
    response = self.__formatToHumanReadableText(eventsFilteredAttributes)
    
    return ActionExecutedResponse(
      hasResponse=True,
      responseText=response
    )
    
  def __formatToHumanReadableText(self, events: List) -> str:
    prePromptText = f'''Você é um módulo de um assistente pessoal mais completo. O seu módulo é responsável por buscar eventos agendados no Google Agenda do usuário. A sua tarefa é receber esses eventos no formato de JSON e transformar em um texto para que o usuário saiba quais eventos estão agendados no período solicitado.
    O período solicitado foi:
     - Início: {self.initTime.get("value")}
     - Fim: {self.finalTime.get("value")}
    Os eventos recebidos foram:'''
    for event in events:
      prePromptText += json.dumps(event, indent=4, ensure_ascii=False) + "\n"
    prePromptText += '''Com base nesses eventos, gere um texto em linguagem natural que descreva cada evento, incluindo título, descrição, horário de início e término. Organize os eventos em ordem cronológica e utilize uma linguagem clara e amigável para facilitar a compreensão do usuário. Cite cada evento de maneira flúida, como se estivesse conversando com o usuário, sem ser robotizado falando cada atributo separadamente.
    Se algum atributo não existir, ignore-o na descrição do evento. Se não houver eventos agendados no período solicitado, informe isso de forma clara ao usuário.
    NÃO utilize nenhuma formatação especial, como listas ou marcadores. Apenas gere um texto corrido. Ele futuramente será lido em voz alta para o usuário através de um sistema de texto para fala.'''
    
    tempChat = ChatHistoryController()
    tempChat.addSystemMessage(prePromptText)
    tempChat.addUserMessage("Por favor, gere o texto descritivo dos eventos agendados.")
    response = tempChat.getResponse()
    return response[-1]["content"]
    
    
    
    