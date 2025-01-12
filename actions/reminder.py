from actions.action import Action
import env
from datetime import datetime

def Reminder(text: str, remiderTime: str):
  print(f"Salvando lembrete: {text} para {remiderTime}")
  

ReminderAction = Action('reminder', 'essa action serve para salvar lembretes do usuário. Parâmetros: 1) text: tipo string - O texto do lembrete do usuário em detalhes que foram ditos. 2) remiderTime: - tipo string - Para quando é o lembrete, formatado como HH:MM:SS - DD/MM/YYYY.', Reminder, str, str)