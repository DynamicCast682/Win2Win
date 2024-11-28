import time

import numpy as np
import pyvirtualcam
import requests

from models import VideoShape

main_machine_ip = "http://127.0.0.1:8960"



while True:
  try:
    video_shape_req = requests.get(f'{main_machine_ip}/video_shape')
    video_shape = VideoShape(**video_shape_req.json())
    print(f'video_shape={video_shape}')
    with pyvirtualcam.Camera(width=video_shape.width, height=video_shape.height, fps=20) as cam:
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
