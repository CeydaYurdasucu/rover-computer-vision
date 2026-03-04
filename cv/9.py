import cv2
import numpy as np

cap = cv2.VideoCapture("yl.mp4")
araba = cv2.CascadeClassifier("car.xml")

if araba.empty():
    print("Cascade dosyası yüklenemedi!")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gri = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cars = araba.detectMultiScale(
        gri,
        scaleFactor=1.1,
        minNeighbors=3
    )

    for (x, y, w, h) in cars:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()