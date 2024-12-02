import os
import socket
import time

import numpy as np
import pyvirtualcam
import requests
from dotenv import load_dotenv
from pyvirtualcam import PixelFormat

from funcs import get_device
from models import VideoShape

load_dotenv()
device = None
backend = None
ip = '127.0.0.1'

if os.environ["vmachine"] == 'YES':
  ip = '192.168.1.100'
  main_machine_ip = f"http://{ip}:8960"
  device = "/dev/video0"
else:
  main_machine_ip = "http://127.0.0.1:8960"

while True:
  try:
    try:
      client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      client_socket.connect((ip, 1684))
    except Exception as e:
      print(e)
      print('Server not found reconnect in 5')
      time.sleep(5)
      continue
    print(f'Connected to {ip}')

    width = int.from_bytes(client_socket.recv(4), byteorder='big')
    height = int.from_bytes(client_socket.recv(4), byteorder='big')

    with pyvirtualcam.Camera(width=width, height=height, fps=20,
                             device=device,
                             fmt=PixelFormat.BGR) as cam:
      while True:
        # Receive image size
        size = int.from_bytes(client_socket.recv(4), byteorder='big')

        # Receive image data
        data = b''
        while len(data) < size:
          packet = client_socket.recv(size - len(data))
          if not packet:
            break
          data += packet

        # Convert bytes to image
        frame = np.frombuffer(data, dtype=np.uint8).reshape((height, width, 3))
        cam.send(frame)
        cam.sleep_until_next_frame()
  except Exception as e:
    print(e)
    print('Global error reconnect in 5')
    time.sleep(5)

# while True:
#   try:
#     print('Trying to get')
#     video_shape_req = requests.get(f'{main_machine_ip}/video_shape')
#     video_shape = VideoShape(**video_shape_req.json())
#     print(f'video_shape={video_shape}')
#     with pyvirtualcam.Camera(width=video_shape.width, height=video_shape.height, fps=20,
#                              device=device,
#                              fmt=PixelFormat.BGR) as cam:
#       print(f'Using virtual camera: {cam.device}')
#
#       while True:
#         video_frame_req = requests.get(f'{main_machine_ip}/video_frame')
#         frame = np.array(video_frame_req.json(), dtype=np.uint8)
#         # print(video_frame)
#         # input()
#         print('frame get')
#         cam.send(frame)
#         cam.sleep_until_next_frame()
#
#
#
#   except Exception as e:
#     print(e)
#     print('sleep 5')
#     time.sleep(5)
