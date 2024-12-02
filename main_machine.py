import socket

import cv2 as opencv
import uvicorn
from fastapi import FastAPI
import keyboard

from Effects.FrameManipulation import FrameManipulation
from Effects.Switch import Switch
from funcs import get_device, SocketFrame, VideoStream
from models import VideoShape

index, backend = get_device('OBS')
print(f'{index=}, {backend=}')
assert index is not None, 'No camera found'

video = opencv.VideoCapture(index, backend)

app = FastAPI()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 1684))
server_socket.listen(1)
print('Сервер ожидает подключения...')


while True:
  try:
    conn, addr = server_socket.accept()
    print(f'Подключено к {addr}')

    vs = VideoStream(video, conn)
    fm = FrameManipulation(vs)
    switch = Switch(vs)

    vs.send_shape()

    for vs_frame in vs:
      # if keyboard.is_pressed('ctrl+shift'):
      #   for switch_frame in switch:
      #     switch_frame.send()
      #   continue

      fm.frame = vs_frame

      fm.random_lags()
      fm.random_lowquality()

      fm.send()


  except Exception as e:
    print(e)
    print('Client disconnected')

# @app.get('/video_shape')
# def get_video_shape() -> VideoShape:
#   return VideoShape(width=width, height=height)
#


# if __name__ == '__main__':
#   uvicorn.run(app, host='192.168.1.100', port=8960)
