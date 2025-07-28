import datetime
from typing import Optional

import cv2
import numpy as np

from Effects.RandomLags import RandomLags
from funcs import SocketFrame, VideoStream




class FrameManipulation:
  def __init__(self, vs: VideoStream):
    self.vs = vs
    self.frame: Optional[SocketFrame] = vs.get()
    self.default_width = vs.width
    self.default_height = vs.height

    self.rl = RandomLags(vs)

  def send(self):
    return self.frame.send()

  def random_lags(self):
    return self.rl.random_lags()


  def random_lowquality(self):
    ...

  def lowquality(self) -> SocketFrame:
    width, height = self.frame.data.shape[1] // 4, self.frame.data.shape[0] // 4
    low_res_frame = cv2.resize(self.frame.data, (width, height), interpolation=cv2.INTER_LINEAR)

    # Повышение уровня сжатия
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 10]  # 10 - очень низкое качество
    result, encimg = cv2.imencode('.jpg', low_res_frame, encode_param)
    if not result:
      return self.frame

    # Декодирование обратно в изображение
    low_quality_frame = cv2.imdecode(encimg, 1)
    low_quality_frame = cv2.resize(low_quality_frame,
                                   (self.default_width, self.default_height),
                                   interpolation=cv2.INTER_LINEAR)
    return SocketFrame(low_quality_frame, self.frame.conn)


class SwitchLags(FrameManipulation):
  def __init__(self, vs: VideoStream, pics_count2switch: int):
    super().__init__(vs)
    self.pics_count2switch = pics_count2switch
    self.pics_part_to_lag = int(self.pics_count2switch / 4)
    self.start_lags = self.pics_part_to_lag
    self.end_lags = self.pics_count2switch - self.start_lags

  def lags_cond(self, iteration: int, last_frame: np.ndarray):
    return iteration <= self.start_lags or iteration >= self.end_lags
