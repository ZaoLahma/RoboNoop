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

        bodies = self.detect_bodies(image)
        faces = self.detect_faces(image)

        return humans

    def detect_faces(self, image):
        faces = self.face_cascade.detectMultiScale(image, 1.1, 4)
        return faces

    def detect_bodies(self, image):
        (rects, weights) = self.hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)
        return rects