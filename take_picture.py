import cv2
import face_recognition
import time
import subprocess
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if face_recognition.face_encodings(frame):
        print("Found")
        filename = str(time.time()).replace(".", "") + ".png"
        cv2.imwrite(filename, frame)
        subprocess.call("mv %s Known_Images/" % filename, shell=True)