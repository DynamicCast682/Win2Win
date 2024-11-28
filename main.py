


# with pyvirtualcam.Camera(width=frame.shape[1], height=frame.shape[0], fps=20) as cam:
#   print(f'Using virtual camera: {cam.device}')
#
#   assert frame.shape == (cam.height, cam.width, 3), f'{frame.shape} != {(cam.height, cam.width, 3)}'
#   # frame = np.zeros((cam.height, cam.width, 3), np.uint8)  # RGB
#   while True:
#     # h, s, v = (cam.frames_sent % 100) / 100, 1.0, 1.0
#     # r, g, b = colorsys.hsv_to_rgb(h, s, v)
#     # frame[:] = (r * 255, g * 255, b * 255)
#
