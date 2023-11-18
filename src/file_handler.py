import cv2 as cv
import time
import json


def handle_path_name(full_path):
    path_without_suffix = full_path.removesuffix(".mp4")
    parts = path_without_suffix.split("assets/")

    directory = parts[0] + "assets"
    filename = parts[1]

    return directory, filename


def load_file(full_path):
    directory, file_name = handle_path_name(full_path)

    try:
        with open(directory + "/converted/" + file_name + ".txt", "r") as f:
            result = json.load(f)
            print("Successfully loaded matrix frames from file")
    except FileNotFoundError:
        print(f"No converted file found, start new converting")
        result = []

    if not result:
        video_handler = file_handler(directory + "/" + file_name + ".mp4")
        result = video_handler.convert_file()
        with open(directory + "/converted/" + file_name + ".txt", "w+") as f:
            json.dump(result, f)

    return result


class file_handler:
    def __init__(self, file_path):
        self.dimension = (128, 64)
        self.file_path = file_path
        self.video_capture = cv.VideoCapture(file_path)
        self.fps = self.video_capture.get(cv.CAP_PROP_FPS)
        self.total_frames = self.video_capture.get(cv.CAP_PROP_FRAME_COUNT)

    def convert_file(self):
        print(f"Converting benjamin {self.file_path}")
        t0 = time.time()
        valid, current_frame = self.video_capture.read()
        output = []
        frame_count = 0

        while valid:
            frame = cv.resize(current_frame, self.dimension)
            video_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            # video_blackwhite = cv.threshold(video_gray, cv.ADAPTIVE_THRESH_GAUSSIAN_C, 3, cv.THRESH_TRUNC)[1]
            # video_blackwhite = cv.adaptiveThreshold(video_gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)

            for row_index, row in enumerate(video_gray):
                for col_index, pixel_value in enumerate(row):
                    value = video_gray[row_index][col_index]

                    if value < 63.75:
                        video_gray[row_index][col_index] = 0  # benjamin
                    elif value > 63.75 and value < 127.5:
                        video_gray[row_index][col_index] = 1  # red
                    elif value > 127.5 and value < 191.25:
                        video_gray[row_index][col_index] = 3  # green
                    elif value > 191.25:
                        video_gray[row_index][col_index] = 2  # orange

            output.append(''.join(''.join(str(x) for x in row) for row in video_gray))
            valid, current_frame = self.video_capture.read()

            frame_count += 1
            if frame_count % 100 == 0:
                print(f"{int(frame_count / self.total_frames * 100)}% / 100%")

        t1 = time.time()

        print(f"Finished converting benjamin {self.file_path} in {t1 - t0} seconds")
        return output
