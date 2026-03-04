import cv2
import numpy as np

img = cv2.imread("yazi.webp")

gri = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gri = np.float32(gri)

# Koseleri buluyoruz
corner = cv2.goodFeaturesToTrack(gri, 50, 0.1, 10)

corner = np.int64(corner)

for c in corner:
    x, y = c.ravel()
    cv2.circle(img, (x, y), 5, (255, 0, 0), -1)

cv2.imshow("u", img)
cv2.waitKey(0)
cv2.destroyAllWindows()