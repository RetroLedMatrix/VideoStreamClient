from src.mqtt_api import mqtt_api
from src.file_handler import file_handler
import time


def send_frames(fps, converted_frames):
    delay = 1.0 / fps

    for frame in converted_frames:
        next_time = time.time() + delay
        time.sleep(max(0, next_time - time.time()))
        mqtt_client.publish(frame)


mqtt_client = mqtt_api("localhost", 9001, "videob/allpixels")
mqtt_client.connect_mqtt()

video_handler = file_handler("../../assets/bad_apple.mp4")
result = video_handler.convert_file()
send_frames(video_handler.fps, result)
