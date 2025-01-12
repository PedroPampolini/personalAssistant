from actions.action import Action
import ctypes

def LockWindows():
  try:
    ctypes.windll.user32.LockWorkStation()
  except Exception as e:
    return f"Erro ao bloquear o computador: {e}"
  

LockWindowsAction = Action('lockWindows', 'Bloqueia o computador windows.', LockWindows)