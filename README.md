# VideoStreamClient
A small python application with converts and plays a video or image file on a 128x64 LED matrix.

## Installation
To install the needed dependencies run the following command:
```
pip install -r requirements.txt
```

To start the application run the following command:
```
python src/frontend/gui.py
```

## Usage
Enter the ip address of the server and the port of the mqtt server in the text fields and press the connect button. If the connection was successful the application will switch to the `Video` tab. An error message will be displayed if the connection was not successful.

Now you can select a video or image file with the `Select File` button, to convert the file to a format that can be displayed on the LED matrix press the `Start conversion` button.

After the conversion is finished a message box will be opened,  you can now press the `Start playback` button to start sending mqtt messages containing the individual frames of the video.

