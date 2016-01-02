import cv2


cap = cv2.VideoCapture(0)
cap_size = (640, 480)
codecs = dict(avc='avc1', mpeg='mp4v', raw='raw ', jpeg='jpeg')

fourcc = cv2.cv.CV_FOURCC(*codecs['mpeg'])
_file = cv2.VideoWriter('output.avi', fourcc, 20.0, cap_size, True)

while cap.isOpened():
    ret_val, frame = cap.read()
    if ret_val is True:
        resized = cv2.resize(frame, cap_size)
        _file.write(resized)
        cv2.imshow('frame', resized)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
_file.release()
cv2.destroyAllWindows()


