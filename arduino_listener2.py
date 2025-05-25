import serial
import time
import os

KOMUT_DOSYASI = "komut.txt"
ser = serial.Serial('COM7', 9600, timeout=1)
time.sleep(2)
son_komut = ""

while True:
    try:
        if os.path.exists(KOMUT_DOSYASI):
            with open(KOMUT_DOSYASI, "r") as file:
                komut = file.read().strip()

            if komut and komut != son_komut:
                print(f"Arduino'ya gönderiliyor: {komut}")
                ser.write((komut + "\n").encode())
                son_komut = komut

        time.sleep(0.5)
    except KeyboardInterrupt:
        print("Durduruldu.")
        break
    except Exception as e:
        print("Hata:", e)
