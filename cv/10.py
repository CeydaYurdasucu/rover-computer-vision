import cv2
import numpy as np
import time


# --- 1. PID SINIFI (Paylaştığın koddan alındı) ---
class PID:
    def __init__(self, Kp, Ki, Kd):
        self.Kp, self.Ki, self.Kd = Kp, Ki, Kd
        self.previous_error = 0
        self.previous_time = time.time()
        self.integral = 0

    def update(self, error):
        current_time = time.time()
        dt = current_time - self.previous_time
        if dt <= 0: return 0

        p = error
        self.integral += error * dt
        d = (error - self.previous_error) / dt

        self.previous_error = error
        self.previous_time = current_time
        return (self.Kp * p) + (self.Ki * self.integral) + (self.Kd * d)


# --- 2. AYARLAR ---
cap = cv2.VideoCapture(0)
my_pid = PID(Kp=0.5, Ki=0.0, Kd=0.1)  # PID katsayıların

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]

    # ROI: Sadece alt kısma bak (Robotun önü)
    roi = frame[int(h * 0.7):h, :]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)  # Siyah çizgiyi bul

    # 3. MERKEZ NOKTASI HESABI (Hata miktarını bulma)
    M = cv2.moments(mask)
    if M["m00"] > 0:
        cx = int(M["m10"] / M["m00"])  # Çizginin merkezi
        ekran_merkezi = w // 2

        # Hata (Error): Çizgi merkezden ne kadar uzakta?
        hata = cx - ekran_merkezi

        # PID GÜNCELLEME
        duzeltme = my_pid.update(hata)

        # MOTOR KOMUTLARI (Sanal)
        sol_motor = 50 + duzeltme
        sag_motor = 50 - duzeltme

        # Ekrana çizimler
        cv2.circle(roi, (cx, 30), 10, (0, 255, 0), -1)
        cv2.line(roi, (ekran_merkezi, 0), (ekran_merkezi, h), (255, 0, 0), 2)
        cv2.putText(frame, f"Hata: {hata}", (10, 30), 1, 1, (0, 0, 255), 2)
        cv2.putText(frame, f"Sol: {int(sol_motor)} Sag: {int(sag_motor)}", (10, 60), 1, 1, (255, 0, 0), 2)

    cv2.imshow("Ceyda Observer MK1 - Sanal Sürüş", frame)
    cv2.imshow("Robotun Gözü (Maske)", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()