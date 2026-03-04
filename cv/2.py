import cv2
import numpy as np


def nothing(x):
    pass


# 1. Siyah ekranı (512, 512, 3) olarak oluşturuyoruz
img = np.zeros((512, 512, 3), np.uint8)
cv2.namedWindow('image')

# 2. Renk Trackbar'ları
cv2.createTrackbar('R', 'image', 0, 255, nothing)
cv2.createTrackbar('G', 'image', 0, 255, nothing)
cv2.createTrackbar('B', 'image', 0, 255, nothing)

# 3. ANAHTAR (Switch) oluşturma
# 0: Kapalı, 1: Açık
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image', 0, 1, nothing)

while True:
    cv2.imshow('image', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Değerleri oku
    r = cv2.getTrackbarPos('R', 'image')
    g = cv2.getTrackbarPos('G', 'image')
    b = cv2.getTrackbarPos('B', 'image')
    s = cv2.getTrackbarPos(switch, 'image')

    # 4. Anahtar kontrolü
    if s == 0:
        img[:] = 0  # Anahtar kapalıyken ekranı siyah tut
    else:
        img[:] = [b, g, r]  # Anahtar açıkken renkleri uygula

cv2.destroyAllWindows()