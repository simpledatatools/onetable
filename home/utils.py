import cv2 as cv


def save_frame_from_video(video_path, millisecond, frame_file_path):
    vidcap = cv.VideoCapture(video_path)

    vidcap.set(cv.CAP_PROP_POS_MSEC, millisecond)

    success, image = vidcap.read()

    # save image to temp file
    cv.imwrite(frame_file_path, image)

    vidcap.release()