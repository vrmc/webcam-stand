import cv2


class Webcam:
    def __init__(self, casc_path):
        self.cap = cv2.VideoCapture(0)
        self.face_casc = cv2.CascadeClassifier(casc_path)

        self.WIDTH = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.HEIGHT = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def detect_faces(self):
        _, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return self.face_casc.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(200, 200)
        )

def main():
    import sys
    import time
    if len(sys.argv) != 2:
        print("usage: {} [cascade filepath]".format(sys.argv[0], file=sys.stderr))
        sys.exit(1)

    webcam = Webcam(sys.argv[1])
    while True:
        _, frame = webcam.cap.read()
        faces = webcam.detect_faces()
        print("Detected {} face(s).".format(len(faces)))
        for x, y, w, h in faces:
            print("Centre of face: ({}, {}), dimensions of face: ({}, {})".format((x + w) / 2, (y + h) / 2, w, h))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('Webcam Output', frame)
        cv2.waitKey(1000)

if __name__ == "__main__":
    main()

