import cv2

# Open the default camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
  print("Error: Could not open camera.")
  exit()

while True:
  # Capture frame-by-frame
  ret, frame = cap.read()

  if not ret:
    print("Error: Could not read frame.")
    break

  # Display the resulting frame
  cv2.imshow('Camera Feed', frame)

  # Break the loop on 'q' key press
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

# Release the capture and close the window
cap.release()
cv2.destroyAllWindows()