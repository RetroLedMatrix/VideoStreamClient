from paho.mqtt import client as mqtt_client
import random


class mqtt_api:
    def __init__(self, ip_address, port, topic):
        self.client = None
        self.ip_address = ip_address
        self.port = port
        self.client_id = f'VideoStreamClient-{random.randint(0, 1000)}'
        self.topic = topic

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(self.client_id, transport="websockets")
        # client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.connect(self.ip_address, self.port)
        self.client = client
        self.client.loop_start()

    def disconnect_mqtt(self):
        self.client.loop_stop()
        self.client.disconnect()
        self.client = None

    def publish(self, message):
        result = self.client.publish(topic=self.topic, payload=message, qos=2)

        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{message}` to topic `{self.topic}`")
        else:
            print(f"Failed to send message to topic {self.topic}")
