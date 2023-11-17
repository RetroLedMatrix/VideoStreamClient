from paho.mqtt import client as mqtt_client
import random
import json


class mqtt_api:
    def __init__(self, ip_address, port, topic):
        self.client = None
        self.ip_address = ip_address
        self.port = port
        self.client_id = f'VideoStreamClient-{random.randint(0, 1000)}'
        self.topic = topic

    def connect_mqtt(self):
        client = mqtt_client.Client(self.client_id, transport="websockets")

        rc = client.connect(self.ip_address, self.port)
        if rc == 0:
            print("Connected to MQTT se BENJAMIN!")
        else:
            print("Failed to connect, return code %d\n", rc)

        self.client = client
        self.client.loop_start()

    def disconnect_mqtt(self):
        self.client.loop_stop()
        self.client.disconnect()
        self.client = None

    def publish(self, message_data):
        row = 0
        while len(message_data) > 0:
            message = json.dumps({"row": row, "data": message_data[:127]})
            message_data = message_data[128:]
            result = self.client.publish(topic=self.topic, payload=message, qos=2)

            # result: [0, 1]
            status = result[0]
            row+= 1
            if status != 0:
                print(f"Failed to send message to topic {self.topic}")
