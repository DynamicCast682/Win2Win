from socket import socket
from typing import Union

import cv2
import numpy as np
from cv2_enumerate_cameras import enumerate_cameras


def get_device(search: str):
  index, backend = None, None
  for camera_info in enumerate_cameras():
    print(f'{camera_info.index}: {camera_info.name}')
    if search in camera_info.name:
      index, backend = camera_info.index, camera_info.backend
      return index, backend
  return None, None


class fwh:
  def __init__(self,
               frame: np.ndarray,
               width: int,
               height: int):
    self.frame = frame
    self.width = width
    self.height = height


class SocketFrame:
  def __init__(self, frame: Union[np.ndarray, "SocketFrame"], conn: socket):
    if type(self) is SocketFrame:
      self.__dict__.update(frame.__dict__)
      return
    self.data = frame
    self.conn = conn
    self.width = self.data.shape[1]
    self.height = self.data.shape[0]

  def copy(self):
    return SocketFrame(self.data.copy(), self.conn)

  def send(self):
    send_data = self.data.tobytes()
    size = len(send_data)
    self.conn.sendall(size.to_bytes(4, byteorder='big'))
    self.conn.sendall(send_data)


class VideoStream:
  def __init__(self,
               video: cv2.VideoCapture, conn: socket):
    self.video = video
    self.conn = conn

    frame = video.read()[1]

    self.width = frame.shape[1]
    self.height = frame.shape[0]

  def send_shape(self):
    self.conn.sendall(self.width.to_bytes(4, byteorder='big'))
    self.conn.sendall(self.height.to_bytes(4, byteorder='big'))

  def __iter__(self):
    return self

  def __next__(self) -> SocketFrame:
    return SocketFrame(self._trywhile(), self.conn)

  def get(self) -> SocketFrame:
    return self._trywhile()

  def _trywhile(self) -> SocketFrame:
    ret, frame = self.video.read()
    while not ret:
      print('Frame not received (ret)')
      ret, frame = self.video.read()
    return SocketFrame(frame, self.conn)
