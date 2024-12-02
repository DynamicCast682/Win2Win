import socket

import cv2 as opencv
import uvicorn
from fastapi import FastAPI

from funcs import get_device
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

    frame = video.read()[1]
    width, height = frame.shape[1], frame.shape[0]
    conn.sendall(width.to_bytes(4, byteorder='big'))
    conn.sendall(height.to_bytes(4, byteorder='big'))

    while True:
      ret, frame = video.read()
      if not ret:
        break

      # Преобразование изображения в байты
      data = frame.tobytes()
      size = len(data)

      # Отправка размера изображения
      conn.sendall(size.to_bytes(4, byteorder='big'))
      conn.sendall(data)
  except Exception as e:
    print(e)
    print('Client disconnected')

# @app.get('/video_shape')
# def get_video_shape() -> VideoShape:
#   return VideoShape(width=width, height=height)
#


# if __name__ == '__main__':
#   uvicorn.run(app, host='192.168.1.100', port=8960)
