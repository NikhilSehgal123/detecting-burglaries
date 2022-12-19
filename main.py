from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import cv2

import dotenv

dotenv.load_dotenv()

'''
Authenticate
Authenticates your credentials and creates a client.
'''
subscription_key = os.getenv("API_KEY")
endpoint = os.getenv("VISION_ENDPOINT")


computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
'''
END - Authenticate
'''

video_path = "videos/ring_footageHD.mp4"

"""
Now let's analyze the video to detect any suspicious activity
"""

# Set a frame counter
frame_counter = 0

# Open the video file
video_capture = cv2.VideoCapture(video_path)

# Read the first frame
success, frame = video_capture.read()

while success:
    # Increment the frame counter
    frame_counter += 1

    # Read only every 5th frame
    if frame_counter % 5 == 0:
        # Save the frame as a JPEG file
        cv2.imwrite("frames/frame%d.jpg" % frame_counter, frame)

        # Get the image URL for the frame
        image_path = "frames/frame%d.jpg" % frame_counter

        # Detect objects in the frame
        detected_objects = computervision_client.detect_objects_in_stream(open(image_path, "rb"))

        # Check first if any objects were detected
        if detected_objects.objects:
            # Check the list of detected objects for suspicious activity
            for obj in detected_objects.objects:
                print(obj)
                if obj.object_property == "person" and obj.confidence > 0.5:
                    print("Analyzing frame %d" % frame_counter)
                    # If a person is detected with a confidence level greater than 50%, send an alert
                    print("******** ALERT!!!!!! Suspicious activity detected: person detected in the footage ********")
                    raise SystemExit
                else:
                    print("Frame %d - Nothing suspicious detected in the footage" % frame_counter)
        else:
            # If no objects were detected, send an alert
            print("Frame %d - Nothing detected in the footage" % frame_counter)

        # Delete the frame
        os.remove(image_path)

    # Read the next frame
    success, frame = video_capture.read()

# Release the video capture object
video_capture.release()


