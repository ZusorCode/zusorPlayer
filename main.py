import face_recognition
from pyzbar.pyzbar import decode
import cv2
import os

cap = cv2.VideoCapture(0)


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
        if not self.manually_authorized and self.deauthorize_countdown >= 20:
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
        for image in os.listdir("Known_Images"):
            for face in face_recognition.face_encodings(face_recognition.load_image_file("Known_Images/%s" % image)):
                self.trusted_face_encodings.append(face)

    def face_check(self):
        converted_screencap = cv2.imread("photoaf.jpg")[:, :, ::-1]
        face_encodings = face_recognition.face_encodings(converted_screencap,
                                                         face_recognition.face_locations(converted_screencap))
        for unknown_face in face_encodings:
            matches = face_recognition.compare_faces(self.trusted_face_encodings, unknown_face)
            if True in matches:
                return True
            return False


def face_check(image):
    rgb_small_frame = image[:, :, ::-1]
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_recognition.face_locations(rgb_small_frame))
    for unknown_face in face_encodings:
        matches = face_recognition.compare_faces(trusted_face_encodings, unknown_face)
        if True in matches:
            return True
    return False


def qr_code_scan():
    decode(cv2.cvtColor(cap.read(), cv2.COLOR_BGR2RGB))


if __name__ == "__main__":
    load_faces()
    # cap = cv2.VideoCapture(0)
    face_scanner = FaceScanner()
    auth_manager = AuthManager()
    auth_manager.face_update()
    print(auth_manager.is_authorized)