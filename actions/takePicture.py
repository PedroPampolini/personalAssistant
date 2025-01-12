from actions.action import Action
import cv2
from uuid import uuid4
import env
import os

def TakePicture():
  camera = cv2.VideoCapture(0)
  filePath = os.path.join(env.TMP_FOLDER_PATH, f'{uuid4()}.jpg')
  ret, frame = camera.read()
  camera.release()
  cv2.imwrite(filePath, frame)

TakePictureAction = Action('takePicture', 'Tira uma foto com a webcam do computador.', TakePicture)
