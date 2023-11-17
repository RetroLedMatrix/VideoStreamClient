import cv2 as cv
import numpy as np
import paho.mqtt.client as mqtt

PALETTE = np.array([[0, 0, 0], [255, 255, 255]])
DIMENSIONS = (128, 64)
def nothing(x): pass


#mqttc = mqtt.Client()
#mqttc.connect("192.168.1.101", port=9001)

# Define a video capture object
cap = cv.VideoCapture("../assets/bad_apple.mp4")
fourcc = cv.VideoWriter_fourcc(*'mp4v')
frametime = int(100/cap.get(cv.CAP_PROP_FPS))


# Capture video frame by frame
ret, frame = cap.read()
cv.namedWindow('adaptive threshold', cv.WINDOW_NORMAL)

flipcode = 1
while ret:
    frame = cv.resize(frame, DIMENSIONS)
    vid_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    vid_bw = cv.threshold(vid_gray, cv.ADAPTIVE_THRESH_GAUSSIAN_C, 2, cv.THRESH_BINARY)[1]
    cv.imshow('adaptive threshold', cv.flip(vid_bw, flipcode))

    if flipcode == 90000:
        with open('frame.txt', 'w+') as f:
            for line in vid_bw:
                f.write(''.join([str(x) for x in line]))
        print("Written")

    message_data = ''.join(''.join(str(x) for x in row) for row in vid_bw)
    #mqttc.publish("videob/allpixels", '{"data":"'+message_data+'"}')

    ret, frame = cap.read()
    if cv.waitKey(frametime) & 0xFF == ord('q'):
        break
    flipcode+=1

if cv.waitKey(1) & 0xFF == ord('q'):
    cap.release()
    cv.destroyAllWindows()

