from threading import Thread

from src.mqtt_api import mqtt_api
from src.file_handler import load_file
import time
import json
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import StringVar, filedialog as fd

DIMENSIONS = (360, 230)

class gui:
    def __init__(self):
        self.mqtt_client = None
        self.file_path = None
        self.converted_frames = None

        # Initialize master GUI window
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.app = ctk.CTk()
        self.app.geometry(f"{DIMENSIONS[0]}x{DIMENSIONS[1]}")

        # Initialize tabviews
        self.tabview = ctk.CTkTabview(self.app, width=DIMENSIONS[0], height=DIMENSIONS[1])
        self.tabview.pack()

        #result = load_file("../../assets/Shrek_1.mp4")
        self.tabview.add("Connection")
        self.tabview.add("Video")
        self.tabview.set("Connection")

        # Initialize video tab
        self.file_label = StringVar()
        self.file_label.set("Selected file: None")

        file_button = ctk.CTkButton(self.tabview.tab("Video"), text="Select File", command=self.select_file)
        file_button.pack(pady=5)
        label = ctk.CTkLabel(self.tabview.tab("Video"), textvariable=self.file_label)
        label.pack()
        clear_button = ctk.CTkButton(
            self.tabview.tab("Video"),
            text="Clear matrix",
            command=lambda: self.mqtt_client.publish({}, "clear")
        )
        clear_button.pack(pady=5)

        self.method_combobox = ctk.CTkComboBox(self.tabview.tab("Video"), values=["color", "binary"])
        self.method_combobox.pack()

        convert_button = ctk.CTkButton(
            self.tabview.tab("Video"),
            text="Start conversion",
            command=self.get_converted_frames
        )
        convert_button.pack(side='left', anchor='e', expand=True)
        playback_button = ctk.CTkButton(
            self.tabview.tab("Video"),
            text="Start playback",
            command=lambda: Thread(target=self.send_frames_to_topic, args=(24, self.converted_frames, "allpixels")).start()
        )
        playback_button.pack(side='right', anchor='w', expand=True)

        # Initialize connection tab
        ip_label = ctk.CTkLabel(self.tabview.tab("Connection"), text="IP Address:")
        ip_label.pack()
        ip_entry = ctk.CTkEntry(self.tabview.tab("Connection"))
        ip_entry.pack()

        prefix_label = ctk.CTkLabel(self.tabview.tab("Connection"), text="Topic Prefix:")
        prefix_label.pack()
        prefix_entry = ctk.CTkEntry(self.tabview.tab("Connection"))
        prefix_entry.pack()

        connect_button = ctk.CTkButton(
            self.tabview.tab("Connection"),
            text="Connect",
            command=lambda: self.connect_mqtt(ip_entry.get(), prefix_entry.get())
        )
        connect_button.pack(pady=10)

        self.app.mainloop()

    def send_frames_to_topic(self, fps, converted_frames, topic):
        delay = 1.0 / fps
        self.configure_brightness(50, "brightnessPercent")

        for frame in converted_frames:
            next_time = time.time() + delay
            time.sleep(max(0, next_time - time.time()))
            self.mqtt_client.publish(frame, topic)

    def select_file(self):
        self.file_path = fd.askopenfilename()
        self.file_label.set(f"Selected benjamin: {self.file_path.split('/')[-1]}")
        self.app.update_idletasks()

    def connect_mqtt(self, ip_address, prefix):
        # Setup MQTT client
        try:
            self.mqtt_client = mqtt_api(ip_address, 9001, prefix)
            self.mqtt_client.connect_mqtt()
            self.tabview.set("Video")
        except Exception:
            CTkMessagebox(title="Error", message="Failed to connect to MQTT server!", icon="cancel")
            print("Failed to connect to MQTT server")

    def get_converted_frames(self):
        self.converted_frames = load_file(self.file_path)

    def configure_brightness(self, percent, topic):
        self.mqtt_client.publish(percent, topic)


if __name__ == "__main__":
    gui()
