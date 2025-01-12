from actions.action import Action
from threading import Thread
import ctypes


def debugPopup(text: str, *args):
  try:
    def showPopup(text):
      ctypes.windll.user32.MessageBoxW(0, text, "Debug", 0)

    Thread(target=showPopup, args=(text,)).start()
  except Exception as e:
    return f"Erro ao exibir popup de debug: {e}"

DebugPopupAction = Action('debugPopup', 'abre um popup/mensgem de debug. Paramêtro 1) text: tipo string - o texto que existirá no corpo do popup.', debugPopup, str)
