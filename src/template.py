import cv2 as cv
import numpy as np
from mqtt_api import mqtt_api
import json
import time

PALETTE = np.array([[0, 0, 0], [255, 255, 255]])
DIMENSIONS = (128, 64)
def nothing(x): pass


mqtt = mqtt_api("localhost", 9001, "videob/allpixels")
mqtt.connect_mqtt()

# Define a video capture object
cap = cv.VideoCapture("../assets/bad_apple.mp4")
frametime = int(1000/cap.get(cv.CAP_PROP_FPS))


# Capture video frame by frame
ret, frame = cap.read()
cv.namedWindow('adaptive threshold', cv.WINDOW_NORMAL)

flipcode = 1
while ret:
    time.sleep(0.1)
    frame = cv.resize(frame, DIMENSIONS)
    vid_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    vid_bw = cv.threshold(vid_gray, cv.ADAPTIVE_THRESH_GAUSSIAN_C, 2, cv.THRESH_BINARY)[1]
    cv.imshow('adaptive threshold', cv.flip(vid_bw, flipcode))

    message = json.dumps({"data": ''.join(''.join(str(x) for x in row) for row in vid_bw)})
    mqtt.publish(message)


    ret, frame = cap.read()
    if cv.waitKey(frametime) & 0xFF == ord('q'):
        break
    flipcode+=1

if cv.waitKey(1) & 0xFF == ord('q'):
    cap.release()
    cv.destroyAllWindows()

mqtt_api.disconnect_mqtt()
