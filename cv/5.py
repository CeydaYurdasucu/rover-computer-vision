import cv2
import numpy as np

# Kamerayı başlatıyoruz
cap = cv2.VideoCapture(0)


def nothing(x):
    pass


# Tek bir kontrol penceresi yerine ayarlar ve görüntü için ayrı pencereler daha iyidir
cv2.namedWindow("Ayarlar")
cv2.resizeWindow("Ayarlar", 640, 480)

# 1. Trackbar Sınırlarını Düzelttik (H: 180, S ve V: 255 olmalı)
cv2.createTrackbar("Alt_H", "Ayarlar", 0, 180, nothing)
cv2.createTrackbar("Alt_S", "Ayarlar", 0, 255, nothing)
cv2.createTrackbar("Alt_V", "Ayarlar", 0, 255, nothing)

# Üst değerleri maksimumdan başlatıyoruz ki görüntü başlangıçta tamamen siyah olmasın
cv2.createTrackbar("Ust_H", "Ayarlar", 180, 180, nothing)
cv2.createTrackbar("Ust_S", "Ayarlar", 255, 255, nothing)
cv2.createTrackbar("Ust_V", "Ayarlar", 255, 255, nothing)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    # Renk maskeleme için HSV dönüşümü şarttır
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 2. Değerleri Doğru Trackbarlardan Okuyoruz (Hatalı değişken eşleşmeleri düzeltildi)
    alt_h = cv2.getTrackbarPos("Alt_H", "Ayarlar")
    alt_s = cv2.getTrackbarPos("Alt_S", "Ayarlar")
    alt_v = cv2.getTrackbarPos("Alt_V", "Ayarlar")

    ust_h = cv2.getTrackbarPos("Ust_H", "Ayarlar")
    ust_s = cv2.getTrackbarPos("Ust_S", "Ayarlar")
    ust_v = cv2.getTrackbarPos("Ust_V", "Ayarlar")

    # Renk aralıklarını NumPy dizisine çeviriyoruz
    alt_renk = np.array([alt_h, alt_s, alt_v])
    ust_renk = np.array([ust_h, ust_s, ust_v])

    # 3. Maskeleme ve Sonuç
    mask = cv2.inRange(frame_hsv, alt_renk, ust_renk)
    # Bitwise AND ile sadece seçilen rengi orijinal renginde görüyoruz
    sonuc = cv2.bitwise_and(frame, frame, mask=mask)

    # Pencereleri ayrı isimlerle gösteriyoruz
    cv2.imshow("Orijinal Goruntu", frame)
    cv2.imshow("Maske (Siyah-Beyaz)", mask)
    cv2.imshow("Filtrelenmis Sonuc", sonuc)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()