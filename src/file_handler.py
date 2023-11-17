import cv2 as cv
import json
import time


class file_handler:
    def __init__(self, file_path):
        self.dimension = (128, 64)
        self.file_path = file_path
        self.video_capture = cv.VideoCapture(file_path)
        self.fps = self.video_capture.get(cv.CAP_PROP_FPS)
        self.total_frames = self.video_capture.get(cv.CAP_PROP_FRAME_COUNT)

    def convert_file(self):
        print(f"Converting file {self.file_path}")
        t0 = time.time()
        valid, current_frame = self.video_capture.read()
        output = []
        frame_count = 0

        while valid:
            frame = cv.resize(current_frame, self.dimension)
            video_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            video_blackwhite = cv.threshold(video_gray, cv.ADAPTIVE_THRESH_GAUSSIAN_C, 2, cv.THRESH_BINARY)[1]

            output.append(''.join(''.join(str(x) for x in row) for row in video_blackwhite))
            valid, current_frame = self.video_capture.read()

            frame_count += 1
            if frame_count % 100 == 0:
                print(f"{frame_count/self.total_frames*100}% / 100%")

        t1 = time.time()

        print(f"Finished converting file {self.file_path} in {t1-t0} seconds")
        return output
