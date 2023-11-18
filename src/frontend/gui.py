from threading import Thread

from src.mqtt_api import mqtt_api
from src.file_handler import load_file
import time
import json
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import StringVar, filedialog as fd

DIMENSIONS = (600, 400)

class gui:
    def __init__(self):
        self.mqtt_client = None
        self.file_path = None
        self.converted_frames = None
        self.progress_bar = None

        # Initialize master GUI window
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.app = ctk.CTk()
        self.app.geometry(f"{DIMENSIONS[0]}x{DIMENSIONS[1]}")
        self.app.maxsize(DIMENSIONS[0], DIMENSIONS[1])

        # Initialize tabviews
        self.tabview = ctk.CTkTabview(self.app, width=DIMENSIONS[0], height=DIMENSIONS[1])
        self.tabview.pack()

        self.tabview.add("Connection")
        self.tabview.add("Video")
        self.tabview.set("Connection")

        # Initialize video tab
        self.file_label = StringVar()
        self.file_label.set("Selected file: None")

        file_button = ctk.CTkButton(self.tabview.tab("Video"), text="Select File", command=self.select_file)
        file_button.grid(row=0, column=0)
        label = ctk.CTkLabel(self.tabview.tab("Video"), textvariable=self.file_label)
        label.grid(row=0, column=1, padx=(20, 0))
        clear_button = ctk.CTkButton(
            self.tabview.tab("Video"),
            text="Clear matrix",
            command=lambda: self.mqtt_client.publish({}, "clear")
        )
        clear_button.place(relx=0.75)

        label = ctk.CTkLabel(self.tabview.tab("Video"), text="Conversion method:")
        label.grid(row=1, column=0, pady=20)
        self.method_combobox = ctk.CTkComboBox(self.tabview.tab("Video"), values=["color", "binary"])
        self.method_combobox.grid(row=1, column=1, padx=(20, 0))

        self.fps = StringVar()
        self.fps.set("24")
        label = ctk.CTkLabel(self.tabview.tab("Video"), text="Playback fps:")
        label.grid(row=2, column=0)
        fps = ctk.CTkEntry(self.tabview.tab("Video"), textvariable=self.fps)
        fps.grid(row=2, column=1, padx=(20, 0))

        convert_button = ctk.CTkButton(
            self.tabview.tab("Video"),
            text="Start conversion",
            command=lambda: Thread(target=self.get_converted_frames).start()
        )
        convert_button.grid(row=3, column=0, pady=20)
        playback_button = ctk.CTkButton(
            self.tabview.tab("Video"),
            text="Start playback",
            command=lambda: Thread(target=self.send_frames_to_topic, args=(int(self.fps.get()), self.converted_frames, "allpixels")).start()
        )
        playback_button.grid(row=3, column=1, padx=(20, 0))
        stop_playback_button = ctk.CTkButton(
            self.tabview.tab("Video"),
            text="Stop playback",
            command=lambda: print("Placeholder: stopping playback")
        )
        stop_playback_button.grid(row=3, column=2, padx=(20, 0))

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
        label = ctk.CTkLabel(self.tabview.tab("Video"), text="Conversion progress:")
        label.grid(row=4, column=0)
        self.progress_bar = ctk.CTkProgressBar(self.tabview.tab("Video"), orientation="horizontal")
        self.progress_bar.grid(row=4, column=1, pady=20)
        self.progress_bar.set(0)
        self.converted_frames = load_file(self.file_path, self.progress_bar)
        label.grid_forget()
        self.progress_bar.grid_forget()
        self.progress_bar = None
        CTkMessagebox(message="Converted file successfully.",
                      icon="check", option_1="OK")

    def configure_brightness(self, percent, topic):
        self.mqtt_client.publish(percent, topic)


if __name__ == "__main__":
    gui()
