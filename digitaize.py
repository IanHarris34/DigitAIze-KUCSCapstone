# Import the required libraries
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model

# Initialize the mediapipe mpHands
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils
# Load the mpHands model
model = load_model('mp_hand_gesture')

# Setup the Webcam
webcamCap = cv2.VideoCapture(0)

while True:
    # Read each frame from the webcam
    _, frame = webcamCap.read()

    x, y, c = frame.shape

    # Flip the frame vertically
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get hand landmark prediction
    result = hands.process(framergb)

    # Add all the hand landmarks into a landmarks list
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for landmark in handslms.landmark:
                landmarkx = int(landmark.x * x)
                landmarky = int(landmark.y * y)
                landmarkz = int(landmark.z * 1000)

                landmarks.append([landmarkx, landmarky, landmarkz])

            # Print out the landmarks for debugging
            print( landmarks )
            # Draw the landmarks on the frame
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

    # Show the final output, with the landmarks drawn on the image.
    cv2.imshow("Output", frame) 


	# If "q" key is pressed, escape from the loop and exit
	# If this is not here, the OS would believe the program is "not responding" and no output would be shown (at least on Windows)
    if cv2.waitKey(1) == ord('q'):
        break

# Close the webcam capture
webcamCap.release()

# Close any active windows
cv2.destroyAllWindows()