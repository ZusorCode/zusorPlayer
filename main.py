import face_recognition
from pyzbar.pyzbar import decode
import cv2
import os
import re
import time
import numpy as np
from tqdm import tqdm
cap = cv2.VideoCapture(0)


#class CapHack:
#    def read(self):
#        return cv2.imread("photoaf.jpg")


class AuthManager:
    def __init__(self):
        self.is_authorized = False
        self.deauthorize_countdown = 0
        self.manually_authorized = False

    def face_update(self):
        if not self.manually_authorized:
            if face_scanner.face_check():
                self.is_authorized = True
                self.deauthorize_countdown = 0
            else:
                self.deauthorize_countdown += 1

    def auto_deauthorize_update(self):
        if not self.manually_authorized and self.deauthorize_countdown >= 10:
            self.deauthorize_countdown = 0
            self.is_authorized = False

    def manual_authorize(self):
        self.manually_authorized = True
        self.is_authorized = True
        self.deauthorize_countdown = 0

    def manual_deauthorize(self):
        self.manually_authorized = False
        self.is_authorized = False
        self.deauthorize_countdown = 0


class FaceScanner:
    def __init__(self):
        self.trusted_face_encodings = []
        for image in tqdm(os.listdir("Known_Images")):
            self.trusted_face_encodings.append(face_recognition.face_encodings(face_recognition.load_image_file(f"Known_Images/{image}"))[0])
            self.face_locations = ""    
    def update_values(self):
        self.ret, self.frame = cap.read()
        self.rgb_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        self.show_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        self.face_locations = face_recognition.face_locations(self.rgb_image)
    
    def face_check(self):
        face_encodings = face_recognition.face_encodings(self.rgb_image, face_recognition.face_locations(self.rgb_image))
        for unknown_face in face_encodings:
            matches = face_recognition.compare_faces(self.trusted_face_encodings, unknown_face)
            if True in matches:
                return True
        return False
        
    def show_faces(self):
        #for (top, right, bottom, left) in self.face_locations:
        #    cv2.rectangle(self.show_image, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.imshow("Frame", self.show_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()

class QRCode:
    def __init__(self):
        self.last_command = 0
        self.command = ""

    def scan_code(self):
        self.command = re.findall(r"Decoded\(data='(.*)', type='.*', .*", decode(cv2.cvtColor(cap.read(), cv2.COLOR_BGR2RGB)))[0]
        if " " in self.command:
            self.execute_complex_command()
        else:
            self.execute_simple_command()

    def execute_simple_command(self):
        if self.command == "startv":
            pass
        if not auth_manager.is_authorized:
            return
        if self.command == "deauth":
            pass
        elif self.command == "stopv":
            pass
        elif self.command == "exit":
            pass
        elif self.command == "shutdown":
            pass

    def execute_complex_command(self):
        split_command = re.findall(r"([^\s]+)(.*)", self.command)
        if not auth_manager.is_authorized:
            return
        if split_command[0] == "auth":
            pass
        elif split_command[0] == "run":
            pass


if __name__ == "__main__":
    # cap = cv2.VideoCapture(0)
    face_scanner = FaceScanner()
    auth_manager = AuthManager()
    while True:
        face_scanner.update_values()
        #auth_manager.face_update()
        #auth_manager.auto_deauthorize_update()
        #print(auth_manager.is_authorized)
        face_scanner.show_faces()