"""Simple demonstration of capturing a single frame and saving it to a file

"""

import cv2
import time

cap = cv2.cv.CaptureFromCAM(0)
time.sleep(0.25)
if cap:
    f = cv2.cv.QueryFrame(cap)
    cv2.cv.SaveImage('test.jpg', f)


