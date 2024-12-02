import os
import time

import numpy as np
import pyvirtualcam
import requests
from dotenv import load_dotenv

from funcs import get_device
from models import VideoShape


load_dotenv()
device = None
backend = None
if os.environ["vmachine"] == 'YES':
  main_machine_ip = "http://192.168.1.100:8960"
  device, backend = get_device('OBS')
  assert device is not None, 'No camera found'
else:
  main_machine_ip = "http://127.0.0.1:8960"



while True:
  try:
    print('Trying to get')
    video_shape_req = requests.get(f'{main_machine_ip}/video_shape')
    video_shape = VideoShape(**video_shape_req.json())
    print(f'video_shape={video_shape}')
    with pyvirtualcam.Camera(width=video_shape.width, height=video_shape.height, fps=20,
                             device=device,
                             backend=backend) as cam:
      print(f'Using virtual camera: {cam.device}')

      while True:
        video_frame_req = requests.get(f'{main_machine_ip}/video_frame')
        frame = np.array(video_frame_req.json(), dtype=np.uint8)
        # print(video_frame)
        # input()
        cam.send(frame)
        cam.sleep_until_next_frame()



  except Exception as e:
    print(e)
    print('sleep 5')
    time.sleep(5)
