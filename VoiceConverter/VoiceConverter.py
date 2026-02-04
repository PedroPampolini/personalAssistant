from TTS.api import TTS
import io
import sounddevice as sd
from typing import *
import os
from gtts import gTTS
from pydub import AudioSegment
import numpy as np


TEXT_TO_SPEECH_MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
VOICE_FILE_NAME = "caitVoz.mp3"

class VoiceConverter:
  def __init__(self, isLowEnd=True):
    self.isLowEnd = isLowEnd
    
    if (not isLowEnd):
      self.ttsModel = TTS(model_name=TEXT_TO_SPEECH_MODEL_NAME)
      self.voiceFilePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voiceData", VOICE_FILE_NAME)
      self.__SAMPLE_RATE = 22050
      self.__BLOCK_SIZE = 1024
      self.audioGen = None
    

  
  # da pra fazer um split dessas frases em frases menores, separadas por virgula, ponto, etc
  # e jogar em uma fila para, no consumo, elas sejam tocadas separadamente
  def Text2Speech(self, text: str):
    if(self.isLowEnd):
      return self.Text2SpeechLowEnd(text)
    return self.Text2SpeechHighEnd(text)
  
  def Text2SpeechLowEnd(self, text: str):
    # gera MP3 em memória
    mp3_fp = io.BytesIO()
    tts = gTTS(text=text, lang="pt-br")
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    
     # decodifica MP3 -> áudio bruto
    audio = AudioSegment.from_file(mp3_fp, format="mp3")
    
    # Increase voice speed
    speedup = 1.25
    audio = audio.speedup(playback_speed=speedup)

    # pitch fake
    pitch=1.0
    audio = audio._spawn(
      audio.raw_data,
      overrides={"frame_rate": int(audio.frame_rate * pitch)}
    ).set_frame_rate(audio.frame_rate)


    samples = np.array(audio.get_array_of_samples()).astype("float32")

    # normaliza (16-bit)
    samples /= 2 ** 15

    # toca
    sd.play(samples, samplerate=audio.frame_rate)
    sd.wait()
  
  def Text2SpeechHighEnd(self, text: str):
    speech = self.ttsModel.tts(
      text=text,
      speaker_wav=self.voiceFilePath,
      split_sentences=True,
      language='pt'
    )
    sd.play(speech, samplerate=self.ttsModel.synthesizer.output_sample_rate)

  def Text2Speech_Old(self, text: str):
    speech = self.ttsModel.tts(
      text=text,
      speaker_wav=self.voiceFilePath,
      language='pt'
    )
    audio = np.array(speech).astype(np.float32)
    self.audioGen = self.__audio_generator(audio, self.__BLOCK_SIZE)
    
    with sd.OutputStream(
      samplerate=self.__SAMPLE_RATE,
      channels=1,
      dtype="float32",
      blocksize=self.__BLOCK_SIZE,
      callback=self.__callback,
    ):
      sd.sleep(10_000)

  def __audio_generator(self, wav, block):
    for i in range(0, len(wav), block):
      yield wav[i:i+block]
      
  def __callback(self, outdata, frames, time, status):
    try:
        chunk = next(self.audioGen)
        outdata[:len(chunk), 0] = chunk
        if len(chunk) < frames:
            outdata[len(chunk):] = 0
    except StopIteration:
        outdata[:] = 0
        raise sd.CallbackStop()


  def Speech2Text(self):
    pass
  
voiceConverterInstance = VoiceConverter()