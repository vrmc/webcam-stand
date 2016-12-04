import cv2
import sys
import time

def main():
    if not len(sys.argv) == 2:
        print("usage: {} [cascade filepath]".format(sys.argv[0]))

    cap = cv2.VideoCapture(0) # reads from first webcam
    casc_path = sys.argv[1] # cascade filepath
    face_casc = cv2.CascadeClassifier(casc_path)

    while True:
        ret, frame = cap.read() # read a frame from cap
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # create a grayscal version of the frame
        faces = face_casc.detectMultiScale(
            gray,
            scaleFactor=1,
            minNeighbors=5,
            minSize=(30, 30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )
        print("Found {} faces".format(len(faces)))

        for (x, y, w, h) in faces:
            # print coordinates of centre of rectangle
            print("centre of face: ({}, {})".format((2*x + w) / 2, (2*y + h) / 2))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Webcam Display", frame)
        cv2.waitkey(1000)

    # cleanup
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
