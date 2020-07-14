import cv2
import numpy as np

font = cv2.FONT_HERSHEY_SIMPLEX


def set_window(w, h):
    cv2.namedWindow('', cv2.WINDOW_FULLSCREEN)
    cv2.setWindowProperty('', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.resizeWindow('', (w, h))


def set_bonding_box(frame, xmin, xmax, ymin, ymax):
    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color=(0, 255, 255))


def set_label(frame, labeltxt, xmin, ymin):
    label_len = len(labeltxt) * 5 + 40
    cv2.rectangle(frame, (xmin - 1, ymin - 1), (xmin + label_len, ymin - 10), (0, 255, 255), -1)


def set_label_text(frame, labeltxt, confidence, xmin, ymin):
    cv2.putText(frame, ' ' + labeltxt + ' ' + str(round(confidence, 2)),
                (xmin, ymin - 2), font, 0.3, (0, 0, 0), 1, cv2.LINE_AA)


def display_show(frame, w, h):
    cv2.rectangle(frame, (0, 0), (w, 25), (0, 0, 0), -1)
    cv2.rectangle(frame, (0, h - 25), (w, h), (0, 0, 0), -1)

    #  ------------------------STEREO VISION----------------------------------------------------------------------
    #  Duplicate and stack frame side by side and show
    frame = np.hstack((frame, frame))
    cv2.imshow('', frame)


def display_destroy():
    cv2.destroyAllWindows()
