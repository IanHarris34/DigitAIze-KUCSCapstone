# Import the required libraries
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
import matplotlib.pyplot as plt
import sys
from tensorflow.keras.models import load_model

landmarkNames = [ "palm", "finger0-0", "finger0-1", "finger0-2", "finger0-3", "finger1-0", "finger1-1", "finger1-2", "finger1-3", "finger2-0", "finger2-1", "finger2-2", "finger2-3", "finger3-0", "finger3-1", "finger3-2", "finger3-3", "finger4-0", "finger4-1", "finger4-2", "finger4-3" ]

outFile = open("landmarks.json", "w")

# Initialize the mediapipe mpHands
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7, static_image_mode=True)
mpDraw = mp.solutions.drawing_utils
# Load the mpHands model
model = load_model('mp_hand_gesture')

fig = plt.figure()

# 
def predict(frame, print_json=False):
    global fig
    x, y, c = frame.shape

    # Clear the plot figure
    plt.clf()
    ax = plt.axes( projection='3d' )
    ax.set_xlim([0, 500])
    ax.set_ylim([0, 500])
    ax.set_zlim([-80, 0])
    plt.show( block=False )
    # Get hand landmark prediction
    result = hands.process(frame)

    # Add all the hand landmarks into a landmarks list
    if result.multi_hand_landmarks:
        landmarks = []
        xPoints = []
        yPoints = []
        zPoints = []
        plt.cla()
        ax.set_xlim([0, 400])
        ax.set_ylim([200, 600])
        ax.set_zlim([-50, 0])
        for handslms in result.multi_hand_landmarks:
            for landmark in handslms.landmark:
                landmarkx = int(landmark.x * x)
                xPoints.append( landmarkx )
                landmarky = int(landmark.y * y)
                yPoints.append( landmarky )
                landmarkz = int(landmark.z * 1000)
                zPoints.append( landmarkz )
                landmarks.append([landmarkx, landmarky, landmarkz])
            ax.scatter( xPoints, yPoints, zPoints, c='green' )
            fig.canvas.draw()
            fig.canvas.flush_events()
            # Print out the landmarks for debugging
            # Print JSON
            if print_json:
                print("{", file=outFile)
                idx = 0
                for landmark in landmarks:
                    print("\t\"" + landmarkNames[ idx ] + "_x\": \"" + str( landmark[0] ) + "\",", file=outFile )
                    print("\t\"" + landmarkNames[ idx ] + "_y\": \"" + str( landmark[1] ) + "\",", file=outFile )
                    print("\t\"" + landmarkNames[ idx ] + "_z\": \"" + str( landmark[2] ) + "\",", file=outFile )
                    idx = idx + 1
                print("}", file=outFile)
            ax.set_title( "Landmarks" )
            
            # Draw the landmarks on the frame
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
    
    return frame


# Given a cv2 image, runs the program
def run_from_image(image):
    
    predict(image, True)


# Given an array of cv2 images, runs the programs
def run_from_video(video):

    for image in video:
        predict(image, True)


# Opens and displays webcam and returns an array of images
def get_video_from_webcam():

    return_video = []
    recording = False

    # Setup the Webcam
    webcamCap = cv2.VideoCapture(0)

    while True:

        # Read each frame from the webcam
        _, frame = webcamCap.read()

        # Flip the frame vertically
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Add the current raw frame to the return_video array
        if recording:
            return_video.append(framergb)

        # Get frame with predictions drawn over it
        frame_with_predictions = predict(framergb, False)

        # Display webcam capture with predictions
        cv2.imshow("Output", frame_with_predictions)
        #cv2.imshow("Output", framergb) 
        #plt.show( block=False )

        if cv2.waitKey(1) == ord('r'):
            recording = True

        # If "q" key is pressed, escape from the loop and exit
        # If this is not here, the OS would believe the program is "not responding" and no output would be shown (at least on Windows)
        if cv2.waitKey(1) == ord('q'):
            break

    # Close the webcam capture
    webcamCap.release()

    # Close any active windows
    cv2.destroyAllWindows()
    plt.show()
    outFile.close()

    return return_video


# Opens and displays webcam and returns the image taken when 'q' is pressed
def get_photo_from_webcam():

    # Setup the Webcam
    webcamCap = cv2.VideoCapture(0)

    while True:

        # Read each frame from the webcam
        _, frame = webcamCap.read()

        # Flip the frame vertically
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get frame with predictions drawn over it
        frame_with_predictions = predict(framergb, False)

        # Display webcam capture with predictions
        cv2.imshow("Output", frame_with_predictions)
        #cv2.imshow("Output", framergb) 
        #plt.show( block=False )
        # If "q" key is pressed, escape from the loop and exit
        # If this is not here, the OS would believe the program is "not responding" and no output would be shown (at least on Windows)
        if cv2.waitKey(1) == ord('q'):
            break

    # Close the webcam capture
    webcamCap.release()

    # Close any active windows
    cv2.destroyAllWindows()
    plt.show()
    outFile.close()

    return framergb

#Check arguments
if( len( sys.argv ) > 1 ):
    #If the argument -livecam is passed, start in webcam mode
    if( sys.argv[ 1 ] == "-livecam" ):
        get_photo_from_webcam()