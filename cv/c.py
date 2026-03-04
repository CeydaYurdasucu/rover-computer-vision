import socket
import struct

# SocketCAN kurulumu
can_socket = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
can_socket.bind(("can0",))

def send_can_frame(can_id, data):
    """
    8 byte'lık veriyi CAN hattına basan fonksiyon.
    """
    # CAN Paketi Yapısı: ID (4 byte) + Uzunluk (1 byte) + Data (8 byte)
    can_frame = struct.pack("=IB3x8s", can_id, len(data), data)
    can_socket.send(can_frame)

# ÖRNEK ANALİZ: Robotun motoruna 'DÖN' komutu gönderme
# ID: 0x123 (Sağ Motor Sürücüsü)
# Data: İlk byte 0x01 (Hız komutu modu), ikinci byte 0x2C (Hız değeri)
example_data = bytes([0x01, 0x2C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
send_can_frame(0x123, example_data)