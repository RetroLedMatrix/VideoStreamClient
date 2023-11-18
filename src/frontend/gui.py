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


mqtt_client = mqtt_api("localhost", 9001, "matrixMarco/pixelrow")
mqtt_client.connect_mqtt()

#with open("../../assets/converted/bad_apple_matrix_frames.txt", "r") as f:
with open("../../assets/converted/Shrek_1.txt", "r") as f:
#with open("../../assets/converted/ForestPeople.txt", "r") as f:
#with open("../../assets/converted/ENA_Auction_Day.txt", "r") as f:
    try:
        result = json.load(f)
        print("Succefully loaded matrix frames from file")
    except:
        result = []

if not result:
    #video_handler = file_handler("../../assets/bad_apple.mp4")
    video_handler = file_handler("../../assets/Shrek_1.mp4")
    #video_handler = file_handler("../../assets/ENA_Auction_Day.mp4")
    #video_handler = file_handler("../../assets/ForestPeople.mp4")
    result = video_handler.convert_file()
    #with open("../../assets/converted/bad_apple_matrix_frames.txt", "w+") as f:
    with open("../../assets/converted/Shrek_1.txt", "w+") as f:
    #with open("../../assets/converted/ENA_Auction_Day.txt", "w+") as f:
    #with open("../../assets/converted/ForestPeople.txt", "w+") as f:
        json.dump(result, f)

send_frames(30, result)
mqtt_client.disconnect_mqtt()
