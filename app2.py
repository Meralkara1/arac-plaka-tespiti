import serial
import time

ser = None

try:
    if "ser" not in globals() or ser is None or not ser.is_open:
        ser = serial.Serial('COM7', 9600, timeout=1)
        time.sleep(2)
        print("✅ Arduino bağlantısı başarılı.")
except Exception as e:
    ser = None
    print("❌ Arduino bağlantısı başarısız:", e)







from flask import Flask, render_template, Response
from ultralytics import YOLO
import easyocr
import cv2
import serial
import os
import time
from datetime import datetime


# Flask başlat
app = Flask(__name__)

# YOLO modeli ve OCR
model = YOLO("runs/detect/train9/weights/best.pt")
reader = easyocr.Reader(['en'])

# Klasörler ve sabitler
KAYITLI_PLAKALAR = ["16 LBT 68"]
PLAKA_KAYIT_DOSYASI = "plaka_kayitlari.txt"
SAVE_DIR = "static/kayitli_plakalar"
os.makedirs(SAVE_DIR, exist_ok=True)

current_plate = ""
son_gonderilen_komut = ""

# Kamera bağlantısı
cap = cv2.VideoCapture("http://192.168.1.35:8080/video")
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

def komut_gonder(komut):
    global son_gonderilen_komut
    if ser:
        try:
            ser.write((komut + "\n").encode())
            print(f"Arduino'ya gönderildi: {komut}")
            son_gonderilen_komut = komut  # İstersen bunu da kaldırabilirsin
        except Exception as e:
            print("Komut gönderilemedi:", e)


def generate():
    global current_plate

    while True:
        success, frame = cap.read()
        if not success:
            continue

        results = model.predict(source=frame, conf=0.5, stream=False)
        annotated_frame = results[0].plot()

        for r in results:
            for box in r.boxes:
                cls_name = r.names[int(box.cls[0])]
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Plaka okuma
                if cls_name == "plaka":
                    plaka_crop = frame[y1:y2, x1:x2]
                    ocr_result = reader.readtext(plaka_crop)
                    if ocr_result:
                        plate_text = ocr_result[0][1].strip()
                        current_plate = plate_text

                        now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                        with open(PLAKA_KAYIT_DOSYASI, "a") as f:
                            f.write(f"{plate_text} - {now}\n")

                        save_path = os.path.join(SAVE_DIR, f"{plate_text}_{now}.jpg")
                        cv2.imwrite(save_path, plaka_crop)

                # Komut mantığı
                elif cls_name == "kamyonet":
                    if current_plate in KAYITLI_PLAKALAR:
                        komut_gonder("KAPI")
                    else:
                        komut_gonder("BUZZER")

                elif cls_name == "araba":
                    komut_gonder("BUZZER")

        # Görüntüyü aktar
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template("index.html", plate=current_plate)

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

