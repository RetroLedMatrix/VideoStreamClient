import json
import time

import cv2 as cv


def handle_path_name(full_path):
    path_without_suffix = full_path.removesuffix(".mp4")
    parts = path_without_suffix.split("assets/")

    directory = parts[0] + "assets"
    filename = parts[1]

    return directory, filename


def load_file(full_path, progress_bar):
    directory, file_name = handle_path_name(full_path)

    try:
        with open(directory + "/converted/" + file_name + ".txt", "r") as f:
            result = json.load(f)
            progress_bar.set(1)
            print("Successfully loaded converted frames from file")
    except FileNotFoundError:
        print(f"No converted frames found, start new converting")
        result = []

    if not result:
        video_handler = file_handler(directory + "/" + file_name + ".mp4")
        result = video_handler.convert_file(progress_bar)
        with open(directory + "/converted/" + file_name + ".txt", "w+") as f:
            json.dump(result, f)

    return result


def load_image(full_path):
    image_handler = file_handler(full_path)
    result = image_handler.convert_image()
    return result


class file_handler:
    def __init__(self, file_path):
        self.total_frames = None
        self.fps = None
        self.video_capture = None
        self.dimension = (128, 64)
        self.file_path = file_path

    def convert_file(self, progress_bar):
        self.video_capture = cv.VideoCapture(self.file_path)
        self.fps = self.video_capture.get(cv.CAP_PROP_FPS)
        self.total_frames = self.video_capture.get(cv.CAP_PROP_FRAME_COUNT)

        print(f"Converting file {self.file_path}")
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
                        video_gray[row_index][col_index] = 0  # off
                    elif 63.75 < value < 127.5:
                        video_gray[row_index][col_index] = 1  # red
                    elif 127.5 < value < 191.25:
                        video_gray[row_index][col_index] = 3  # green
                    elif value > 191.25:
                        video_gray[row_index][col_index] = 2  # orange

            output.append(''.join(''.join(str(x) for x in row) for row in video_gray))
            valid, current_frame = self.video_capture.read()

            frame_count += 1
            progress_bar.set(frame_count / self.total_frames)
            if frame_count % 100 == 0:
                print(f"{int(frame_count / self.total_frames * 100)}% / 100%")

        t1 = time.time()

        print(f"Finished converting file {self.file_path} in {t1 - t0} seconds")
        return output

    def convert_image(self):
        print(f"Converting image {self.file_path}")
        t0 = time.time()
        current_frame = cv.imread(self.file_path)
        output = []
        frame = cv.resize(current_frame, self.dimension)
        image_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        for row_index, row in enumerate(image_gray):
            for col_index, pixel_value in enumerate(row):
                value = image_gray[row_index][col_index]

                if value < 63.75:
                    image_gray[row_index][col_index] = 0  # off
                elif 63.75 < value < 127.5:
                    image_gray[row_index][col_index] = 1  # red
                elif 127.5 < value < 191.25:
                    image_gray[row_index][col_index] = 3  # green
                elif value > 191.25:
                    image_gray[row_index][col_index] = 2  # orange

        output.append(''.join(''.join(str(x) for x in row) for row in image_gray))

        t1 = time.time()

        print(f"Finished converting image {self.file_path} in {t1 - t0} seconds")
        return output
