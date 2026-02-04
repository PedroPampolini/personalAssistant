from TTS.api import TTS
import sounddevice as sd
import os

TEXT_TO_SPEECH_MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
VOICE_FILE_NAME = "caitVoz.mp3"

class VoiceConverter:
  def __init__(self):
    self.ttsModel = TTS(model_name=TEXT_TO_SPEECH_MODEL_NAME)
    self.voiceFilePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voiceData", VOICE_FILE_NAME)
    if (os.path.exists(self.voiceFilePath)):
      print("path exists")
    else:
      print("fudeu")
  
  # da pra fazer um split dessas frases em frases menores, separadas por virgula, ponto, etc
  # e jogar em uma fila para, no consumo, elas sejam tocadas separadamente
  def Text2Speech(self, text: str):
    speech = self.ttsModel.tts(
      text=text,
      speaker_wav=self.voiceFilePath,
      split_sentences=True,
      language='pt'
    )
    sd.play(speech, samplerate=self.ttsModel.synthesizer.output_sample_rate)
  
  def Speech2Text(self):
    pass
  
voiceConverterInstance = VoiceConverter()