import cv2
import face_recognition
import time
import subprocess
from tqdm import tqdm, trange
cap = cv2.VideoCapture(0)
for i in trange(10):
    done = False
    while not done:
        ret, frame = cap.read()
        if face_recognition.face_encodings(frame):
            done = True
            filename = str(time.time()).replace(".", "") + ".png"
            cv2.imwrite(filename, frame)
            subprocess.call("mv %s Known_Images/" % filename, shell=True)