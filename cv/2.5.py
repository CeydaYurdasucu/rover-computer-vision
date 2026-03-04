import cv2
import numpy as np


# Boş fonksiyon (Trackbar için zorunlu)
def nothing(x):
    pass


# 1. Kamera ve Pencere Hazırlığı
cap = cv2.VideoCapture(0)
cv2.namedWindow("Ceyda Kontrol Paneli")

# 2. Trackbar'ları Oluştur (Canny Eşik Değerleri İçin)
cv2.createTrackbar("Alt_Esik", "Ceyda Kontrol Paneli", 100, 500, nothing)
cv2.createTrackbar("Ust_Esik", "Ceyda Kontrol Paneli", 200, 500, nothing)
cv2.createTrackbar("Switch", "Ceyda Kontrol Paneli", 0, 1, nothing)

print("Panel Hazır. 'q' ile çıkabilirsiniz.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 3. Trackbar Değerlerini Anlık Oku
    alt = cv2.getTrackbarPos("Alt_Esik", "Ceyda Kontrol Paneli")
    ust = cv2.getTrackbarPos("Ust_Esik", "Ceyda Kontrol Paneli")
    s = cv2.getTrackbarPos("Switch", "Ceyda Kontrol Paneli")

    # 4. Anahtar Kontrolü ve İşleme
    if s == 0:
        # Anahtar kapalıyken normal görüntüyü göster
        cv2.imshow("Ceyda Kontrol Paneli", frame)
    else:
        # Anahtar açıkken canlı ayarlanan değerlerle Canny uygula
        edges = cv2.Canny(gray, alt, ust)
        cv2.imshow("Ceyda Kontrol Paneli", edges)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()