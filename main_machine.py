import cv2 as opencv
from cv2_enumerate_cameras import enumerate_cameras
from fastapi import FastAPI
import uvicorn

from funcs import get_device
from models import VideoShape

app = FastAPI()

index, backend = get_device('OBS')
print(f'{index=}, {backend=}')
assert index is not None, 'No camera found'

video = opencv.VideoCapture(index, backend)
isTrue, frame = video.read()
width, height = frame.shape[1], frame.shape[0]


@app.get('/video_shape')
def get_video_shape() -> VideoShape:
  return VideoShape(width=width, height=height)


@app.get('/video_frame')
def get_video_frame():
  frame = video.read()[1]
  return frame.tolist()

if __name__ == '__main__':
  uvicorn.run(app, host='192.168.1.100', port=8960)
