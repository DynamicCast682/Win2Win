from cv2_enumerate_cameras import enumerate_cameras


def get_device(search: str):
  index, backend = None, None
  for camera_info in enumerate_cameras():
    print(f'{camera_info.index}: {camera_info.name}')
    if search in camera_info.name:
      index, backend = camera_info.index, camera_info.backend
      return index, backend
  return None, None