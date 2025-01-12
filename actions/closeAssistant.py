from actions.action import Action

def CloseAssistant():
  try:
    exit()
    
  except Exception as e:
    return f"Erro ao fechar a execução do programa da assistente virtual: {e}"
  

CloseAssistantAction = Action('closeAssistant', 'Fecha a execução do programa da assitente virtual.', CloseAssistant)