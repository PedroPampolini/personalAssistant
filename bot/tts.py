from utils import debug
import os
import subprocess
from gtts import gTTS
import env

def say(text: str):
  audio_file_path = os.path.join(env.TMP_FOLDER_PATH, 'speech.mp3')
  debug("Convertentdo o audio...")
  try:
    speech = gTTS(text=text, lang=env.LANGUAGE, slow=False)
    speech.save(audio_file_path)
    subprocess.call(["ffplay", "-nodisp", "-autoexit", audio_file_path])
  except Exception as e:
    debug(f"Erro ao enviar o audio do texto:\n{e}")
  