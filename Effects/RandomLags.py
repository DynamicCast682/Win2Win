import datetime
import random

import numpy as np

from funcs import VideoStream


class Active:
  def __init__(self):
    self.start_time = None
    self.end_time = None
    self.finish_timedelta = datetime.timedelta(
      seconds=random.randint(1, 5)
    )

  @property
  def is_active(self):
    if self.start_time is None or self.end_time is None:
      return False
    return datetime.datetime.now() > self.end_time

  def activate(self):
    self.start_time = datetime.datetime.now()
    self.end_time = self.start_time + self.finish_timedelta


class RandomLags:
  chance = 0.3

  def __init__(self, vs: VideoStream):
    self.vs = vs
    self.frame = vs.get()
    self.last_frame = self.frame.copy()

    self.active = Active()

    self.random_lags = self.last_frame_changer(self.random_lags)

  # @staticmethod
  def last_frame_changer(self, func):
    def inner(*args, **kwargs):
      result = func(self, *args, **kwargs)
      self.last_frame = self.frame.copy()
      self.frame = self.vs.get()
      return result
    return inner

  def random_lags(self):
    if self.active.is_active:
      return self.last_frame
    elif np.random.rand() < self.chance:
      self.active.activate()
      return self.last_frame
    return self.frame
