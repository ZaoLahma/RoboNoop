from ....core.log.log import Log

import cv2

class HumanDetector():
    def __init__(self):
        Log.log("HumanDetector created")
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def detect_humans(self, image):
        humans = []

        return humans