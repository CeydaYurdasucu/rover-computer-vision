import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    # Görüntü boyutunu alalım (Genelde 640x480)
    height, width = frame.shape[:2]

    # 1. ROI Koordinatlarını Belirleyelim (Alt kısım, yani yol)
    # Görüntünün ortasından başlayıp en altına kadar giden bir kutu
    roi_ust_kenar = int(height * 0.6)  # Görüntünün %60'ından aşağısı
    roi_alt_kenar = height
    roi_sol_kenar = 0
    roi_sag_kenar = width

    # 2. Görüntüyü Kesme (Slicing/Dilimleme)
    # [y1:y2, x1:x2] formatında
    roi_frame = frame[roi_ust_kenar:roi_alt_kenar, roi_sol_kenar:roi_sag_kenar]

    # 3. Kestiğimiz Bölgeyi Ekranda Bir Kutu İçine Alalım (Görsel Kanıt)
    cv2.rectangle(frame, (roi_sol_kenar, roi_ust_kenar), (roi_sag_kenar, roi_alt_kenar), (0, 255, 0), 2)
    cv2.putText(frame, "ISLEME ALANI (ROI)", (roi_sol_kenar + 10, roi_ust_kenar - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # 4. Sadece Kesilen Bölgeye Canny Uygulayalım (Hız kazandırır!)
    roi_gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)
    roi_edges = cv2.Canny(roi_gray, 100, 200)

    # Pencereleri gösterelim
    cv2.imshow("Ham Goruntu ve ROI Kutusu", frame)
    cv2.imshow("Sadece Yol (Kenar Tespiti)", roi_edges)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()