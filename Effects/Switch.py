import cv2
from cv2 import VideoCapture

from Effects.FrameManipulation import SwitchLags
from funcs import get_device, VideoStream, SocketFrame


class NormalCamera:
  index, backend = get_device('Integrated')
  print(f'Normal Camera {index=}, {backend=}')
  assert index is not None, 'No camera found'

  normal_video = cv2.VideoCapture(index, backend)


class Switch(SwitchLags, NormalCamera):
  pics_count = 120

  def __init__(self,
               vs: VideoStream):
    self.vs = vs

    SwitchLags.__init__(self, vs.width, vs.height, self.pics_count)

    self.last_frame = self.frame.copy()
    self.iteration = 0

  def __iter__(self):
    self.iteration = 0
    return self

  def __next__(self):
    result = self.stop_frame()

    self.last_frame = result.copy()
    self.frame = self.vs.get()
    self.iteration += 1
    return result

  def stop_frame(self):
    if self.lags_cond(self.iteration, self.last_frame):
      return self.last_frame
    return self.frame
