import cv2
import numpy as np
import serial
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
HSV_MIN = np.array(list(map(int, os.getenv('HSV_MIN').split(','))))
HSV_MAX = np.array(list(map(int, os.getenv('HSV_MAX').split(','))))
REF_DISTANCE = int(os.getenv('REF_DISTANCE'))
REF_AREA = int(os.getenv('REF_AREA'))
MIN_SIZE = int(os.getenv('MIN_SIZE'))

# Serial setup
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Update COM port as needed

# Camera setup
cap = cv2.VideoCapture(0)
width, height = 640, 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


def send_command(cmd):
    ser.write(f"{cmd}\n".encode())
    while ser.readline().decode().strip() != 'READY':
        pass


while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, HSV_MIN, HSV_MAX)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    x, y, area, distance = 0, 0, 0, 0
    if contours:
        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)
        if area > MIN_SIZE:
            M = cv2.moments(largest)
            if M['m00'] != 0:
                x = int(M['m10'] / M['m00'])
                y = int(M['m01'] / M['m00'])
                distance = REF_DISTANCE * (REF_AREA / area) ** 0.5

                # Normalize coordinates
                norm_x = (x - width // 2) / (width // 2)
                norm_y = (height // 2 - y) / (height // 2)

                # Send movement commands
                cmd = f"X{norm_x:.2f} Y{norm_y:.2f}"
                send_command(cmd)

    # Draw UI
    cv2.line(frame, (width // 2, 0), (width // 2, height), (0, 255, 0), 1)
    cv2.line(frame, (0, height // 2), (width, height // 2), (0, 255, 0), 1)
    cv2.putText(frame, f"X: {x} Y: {y}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.putText(frame, f"Distance: {distance:.1f}mm", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.putText(frame, f"Area: {area}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow('Frame', frame)
    cv2.imshow('Mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()