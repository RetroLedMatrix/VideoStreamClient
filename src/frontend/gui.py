from src.mqtt_api import mqtt_api
from src.file_handler import load_file
import time


def configure_brightness(percent, topic):
    mqtt_client.publish(percent, topic)


def send_frames_to_topic(fps, converted_frames, topic):
    delay = 1.0 / fps
    for frame in converted_frames:
        next_time = time.time() + delay
        time.sleep(max(0, next_time - time.time()))
        mqtt_client.publish(frame, topic)


mqtt_client = mqtt_api("192.168.1.101", 9001, "matrix")
mqtt_client.connect_mqtt()

# "../../assets/converted/bad_apple_matrix_frames.txt"
# "../../assets/converted/ForestPeople.txt"
# "../../assets/converted/ENA_Auction_Day.txt"

result = load_file("../../assets/Shrek_1.mp4")

configure_brightness(50, "brightnessPercent")
send_frames_to_topic(2, result, "allpixels")
mqtt_client.disconnect_mqtt()
