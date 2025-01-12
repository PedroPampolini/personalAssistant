from datetime import datetime

def buildTimeInfoContext():
  day = datetime.now().day
  month = datetime.now().month
  year = datetime.now().year
  weekday = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo'][datetime.now().weekday()]

  hour = datetime.now().hour
  minute = datetime.now().minute

  contextText = ''
  contextText += f"- dia: {day}\n"
  contextText += f"- mês: {month}\n"
  contextText += f"- ano: {year}\n"
  contextText += f"- dia da semana: {weekday}\n"
  contextText += f"- hora: {hour}\n"
  contextText += f"- minuto: {minute}\n"

  return contextText

context = buildTimeInfoContext()