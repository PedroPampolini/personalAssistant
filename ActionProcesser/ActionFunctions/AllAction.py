from ActionProcesser.ActionFunctions.GetScheduledEvents import GetScheduledEventsAction
from ActionProcesser.ActionFunctions.JustChat import JustChatAction
from ActionProcesser.ActionFunctions.SendWhatsapp import SendWhatsappAction
from ActionProcesser.ActionFunctions.CreateReminder import CreateReminderAction
from ActionProcesser.ActionFunctions.SearchWeb import SearchWebAction

justChatActionInstance = JustChatAction()
sendWhatsappActionInstance = SendWhatsappAction()
createReminderActionInstance = CreateReminderAction()
getScheduledEventsActionInstance = GetScheduledEventsAction()
searchWebActionInstance = SearchWebAction()

ALL_ACTION_FUNCTIONS = [
  justChatActionInstance,
  sendWhatsappActionInstance,
  createReminderActionInstance,
  searchWebActionInstance,
  getScheduledEventsActionInstance
]

ALL_FUNCTIONS_MAP = {
  action.name(): action for action in ALL_ACTION_FUNCTIONS
}

def buildActionsText() -> str:
  actionsListText = ""
  allActions = ALL_ACTION_FUNCTIONS
  for action in allActions:
    actionText = f'- "{action.name()}": {action.description()}\n'
    parametersDescription = action.getParametersDescription()
    parametersText = ""
    for parameter in parametersDescription:
      parametersText += f'    - "{parameter["name"]}" ({parameter["type"]}): {parameter["description"]}\n'
    actionText += f'  Parâmetros:\n{parametersText}'
    actionsListText += actionText + "\n"
    
  return actionsListText


    

