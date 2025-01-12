from actions.action import Action
import env
from datetime import datetime

def SaveLog(text: str):
  try:
    with open(env.LOG_FILE_PATH, 'a') as file:
      file.write(f"[{datetime.now()}] {text}\n")
  except Exception as e:
    return f"Erro ao salvar log: {e}"
  

SaveLogAction = Action('saveLog', 'essa action basicamente salva um texto em um arquivo de log. Parâmetros: 1) text: tipo string - O texto que será salvo no log.', SaveLog, str)