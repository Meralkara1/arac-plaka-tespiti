from ultralytics import YOLO
import cv2

model = YOLO("runs/detect/train9/weights/best.pt")
cap = cv2.VideoCapture("http://192.168.1.35:8080/video")  # Burayı kendi IP'nle değiştir

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(source=frame, show=True, conf=0.5)

    if cv2.waitKey(1) == 27:  # ESC tuşu
        break

cap.release()
cv2.destroyAllWindows()
