import cv2

# 1. Kamera Bağlantısı
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# 2. Kayıt Dosyası ve Format Ayarları

dosyaadi = "C:/video/1.avi"
codec = cv2.VideoWriter_fourcc('W', 'M', 'V', '2')  # WMV2 formatı
framerate = 30
resolution = (640, 480)

# VideoWriter nesnesini oluşturuyoruz
output = cv2.VideoWriter(dosyaadi, codec, framerate, resolution)

print("Kayıt başladı... Durdurmak için 'q' tuşuna basın.")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Görüntü alınamadı.")
        break

    # Görüntüyü kayıt çözünürlüğüne uydur
    frame = cv2.resize(frame, resolution)

    # Robot yönü için aynalama (Flipping)
    frame = cv2.flip(frame, -1)

    # 3. GÖRÜNTÜYÜ DİSKE YAZ
    output.write(frame)

    # Ekranda canlı izle
    cv2.imshow("Webcam Kayit Sistemi", frame)

    # 'q' tuşuna basınca döngüden çık
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 4. Bağlantıları güvenli bir şekilde kapat
cap.release()
output.release()  # Bu satır olmazsa video dosyası bozuk olur!
cv2.destroyAllWindows()

print(f"Video başarıyla şuraya kaydedildi: {dosyaadi}")