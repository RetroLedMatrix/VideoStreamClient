from src.mqtt_api import mqtt_api
from src.file_handler import file_handler
import time
import json


def send_frames(fps, converted_frames):
    delay = 1.0 / fps
    for frame in converted_frames:
        next_time = time.time() + delay
        time.sleep(max(0, next_time - time.time()))
        mqtt_client.publish(frame)


mqtt_client = mqtt_api("192.168.1.101", 9001, "matrix/pixelrow")
mqtt_client.connect_mqtt()

with open("../../assets/converted/bad_apple_matrix_frames.txt", "r") as f:
    try:
        result = json.load(f)
        print("Succefully loaded matrix frames from file")
    except:
        result = []


if not result:
    video_handler = file_handler("../../assets/bad_apple.mp4")
    result = video_handler.convert_file()
    with open("../../assets/converted/bad_apple_matrix_frames.txt", "w+") as f:
        json.dump(result, f)

send_frames(1, result)
mqtt_client.disconnect_mqtt()
