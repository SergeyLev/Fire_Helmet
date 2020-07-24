import sys

import cv2
import time
from multiprocessing import Process
from multiprocessing import Queue

from PIL import Image

from screen import Screen
from camera import MyCamera, RawCapture
from labels import Labels
from classify import classify_frame
from display import set_window, set_bonding_box, set_label, set_label_text, display_show, display_destroy
from iot_watson import IoT

# Misc vars
queuepulls = 0.0
detections = 0
label_txt = None
fps = 0.0
qfps = 0.0
confThreshold = 0.75

#  -------------------------------------------SCREEN SIZE-------------------------------------------------------------
screen = Screen()
#  -------------------------------------------------------------------------------------------------------------------

#  --------------------------------------------CAMERA-----------------------------------------------------------------
#  Initialize the camera and grab a reference to the raw camera capture
camera = MyCamera(screen.resolution.width, screen.resolution.height)
rawCapture = RawCapture(camera.my_camera, screen.resolution.width, screen.resolution.height)
#  -------------------------------------------------------------------------------------------------------------------

#  ---------------------------------------------OD LABELS-------------------------------------------------------------
labels = Labels()
#  -------------------------------------------------------------------------------------------------------------------

# noinspection PyBroadException
try:
    #  -----------------------------------DISPLAY WINDOW--------------------------------------------------------------
    set_window(screen.resolution.width, screen.resolution.height)
    #  ---------------------------------------------------------------------------------------------------------------

    #  ----------------------------------INPUT(FRAME)/OUTPUT(RESULT DATA)---------------------------------------------
    #  Initialize the input queue (frames), output queue (out),
    #  and the list of actual detections returned by the detection thread
    inputQueue = Queue(maxsize=1)
    outputQueue = Queue(maxsize=1)
    img = None
    out = None
    #  ---------------------------------------------------------------------------------------------------------------

    #  ---------------------------------DETECTION THREAD--------------------------------------------------------------
    #  Create detection thread to run independent from main
    detection_thread = Process(target=classify_frame, args=(inputQueue, outputQueue,))
    detection_thread.daemon = True
    detection_thread.start()
    #  ---------------------------------------------------------------------------------------------------------------

    #  ---------------------------------IoT---------------------------------------------------------------------------
    #  Connect to cloud
    iot = IoT()
    #  ---------------------------------------------------------------------------------------------------------------

    #  ----------------------------------FRAME RATE-------------------------------------------------------------------
    timer1 = time.time()
    frames = 0
    queuepulls = 0
    timer2 = 0.
    t2secs = 0.
    #  ---------------------------------------------------------------------------------------------------------------

    #  ----------------------------------CAMERA FRAMES----------------------------------------------------------------
    for frame in camera.my_camera.capture_continuous(rawCapture.rawCapture, format="bgr", use_video_port=True):
        if queuepulls == 1:
            timer2 = time.time()
        #  Capture frame-by-frame
        frame = frame.array

        img = Image.fromarray(frame)

        #  If the input queue is empty, give the current frame to CLASSIFICATION
        if inputQueue.empty():
            inputQueue.put(img)

        #  If the output queue is not empty, grab the CLASSIFICATION result
        if not outputQueue.empty():
            out = outputQueue.get()

        #  Use CLASSIFICATION data
        if out is not None:
            #  Loop over the detections
            for detection in out:
                if detection[0] == 0 or detection[0] == 16 or detection[0] == 17:
                    objID = detection[0]
                    label_txt = labels.my_labels[objID]
                    confidence = detection[1]
                    xmin = detection[2]
                    ymin = detection[3]
                    xmax = detection[4]
                    ymax = detection[5]
                    if confidence > confThreshold:
                        set_bonding_box(frame, xmin, xmax, ymin, ymax)
                        set_label(frame, label_txt, xmin, ymin)
                        set_label_text(frame, label_txt, confidence, xmin, ymin)
                        #  Positive detections per frame not object
                        detections = True
                    else:
                        detections = False
                        label_txt = None

            queuepulls += 1

        #  Display the resulting frame
        display_show(frame, screen.resolution.width, screen.resolution.height)
        #  -----------------------------------------------------------------------------------------------------------

        #  FPS calculation
        frames += 1
        if frames >= 1:
            end1 = time.time()
            t1secs = end1 - timer1
            fps = round(frames / t1secs, 2)
        if queuepulls > 1:
            end2 = time.time()
            t2secs = end2 - timer2
            qfps = round(queuepulls / t2secs, 2)

        #iot.send_data(fps, detections, label_txt)
        #  Clear the stream in preparation for the next frame
        rawCapture.rawCapture.truncate(0)

        #  ------------------------------------CONTROLS---------------------------------------------------------------
        keyPress = cv2.waitKey(1)
        if keyPress == 113:  # q
            break
        if keyPress == 82:  # R
            confThreshold += 0.1
        if keyPress == 84:  # T
            confThreshold -= 0.1
        if confThreshold > 1:
            confThreshold = 1
        if confThreshold < 0.4:
            confThreshold = 0.4
        #  ----------------------------------------------------------------------------------------------------------

    #  ----------------------------------------CLOSE WINDOW AND CAMERA-----------------------------------------------
    display_destroy()
    camera.my_camera.close()
    iot.disconnect_client()
except:
    print("Unexpected error:", sys.exc_info()[0])
    display_destroy()
    camera.my_camera.close()
