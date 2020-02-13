from flask_opencv_streamer.streamer import Streamer
import cv2


def stream_frame(frame):
    port = 5803
    require_login = False
    streamer = Streamer(port, require_login)

    while True:
        streamer.update_frame(frame)

        if not streamer.is_streaming:
            streamer.start_streaming()

        cv2.waitKey(30)