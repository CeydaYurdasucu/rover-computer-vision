import cv2
import numpy as np
import math

# 1. Başlangıç Ayarları
cap = cv2.VideoCapture(0)
frame_genislik = 320  # Hız için düşük çözünürlük
frame_yukseklik = 240
merkez_x = frame_genislik // 2  # Hedefimiz olan tam orta nokta (160)

while True:
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.resize(frame, (frame_genislik, frame_yukseklik))
    frame = cv2.flip(frame, 1)

    # 2. ROI (Region of Interest) - Sadece alt kısma odaklan
    roi = frame[140:240, :]  # Görüntünün alt yarısı
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Meyve suyu kutusu için renk maskesi (Örn: Turuncu/Kırmızı)
    alt_renk = np.array([0, 100, 100])
    ust_renk = np.array([10, 255, 255])
    maske = cv2.inRange(hsv, alt_renk, ust_renk)

    # 3. Moment Analizi ile Merkez (Centroid) Bulma
    M = cv2.moments(maske)
    if M["m00"] > 0:
        cx = int(M["m10"] / M["m00"])  # Kutunun yatay merkezi
        cy = int(M["m01"] / M["m00"])  # Kutunun dikey merkezi

        # 4. Açı (Theta) Hesaplama
        # Kutunun merkezden kaç piksel saptığını bulup açıya çeviriyoruz
        fark = cx - merkez_x
        # math.atan2(karşı, komşu) ile radyan bulup dereceye çeviriyoruz
        acı_radyan = math.atan2(fark, 150)
        acı_derece = int(acı_radyan * 180 / 3.1416)

        # 5. Görselleştirme
        cv2.circle(roi, (cx, cy), 7, (255, 0, 0), -1)  # Kutunun merkezi
        cv2.line(roi, (merkez_x, 0), (merkez_x, 100), (0, 255, 0), 2)  # Hedef çizgi

        # Arduino'ya gönderilecek veri (Simülasyon)
        print(f"Arduino'ya giden komut: Açı {acı_derece} derece")  #
        cv2.putText(frame, f"Aci: {acı_derece}", (10, 30), 1, 1.5, (0, 0, 255), 2)

    cv2.imshow("Ceyda Observer - Navigasyon", frame)
    cv2.imshow("Robotun Maskesi", maske)

    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()