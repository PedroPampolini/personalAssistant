from ActionProcesser.ActionProcesser import actionProcesserInstance

class Middleware:
  '''Classe responsável por intermediar a comunicação entre o usuário e o bot.'''
  
  def sendToBot(text: str) -> str:
    try:
      response = actionProcesserInstance.processAction(text)
      return response
    except Exception as e:
      return f"Houve um erro ao executar o bot: {str(e)}"
    