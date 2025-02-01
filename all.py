import mediapipe as mp
import cv2
import serial
from time import sleep

# Настройка подключения к камере
camera = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# Настройка подключения к Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600)
sleep(2)  # Ждем пару секунд, чтобы плата успела инициализироваться

p = [0 for i in range(21)]
finger = [0 for i in range(5)]

# Функция определения дистанции м/у пальцами
def distance(point1, point2):
    return abs(point1 - point2)

# Подать команду на Arduino
def send_command(command):
    ser.write(bytes(command + '\n', 'utf-8'))

while True:
    # условие соприкосновения пальцев (место для полета фантазии)
    if distance(p[8], p[4]) < 10:
        send_command('H')
        print("H")

    elif distance(p[8], p[4]) > 50:
        send_command('L')
        print("L")

    good, img = camera.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            # получаем размеры изображения с камеры и масштабируем
            for id, point in enumerate(handLms.landmark):
                widht, height, color = img.shape
                widht, height = int(point.x * height), int(point.y * widht)

                # заполняем массив высотой каждой точки
                p[id] = height

                # красим кончики пальцев в красный
                if id == 8:
                    cv2.circle(img, (widht, height), 7, (200, 0, 255), cv2.FILLED)
                if id == 4:
                    cv2.circle(img, (widht, height), 7, (200, 0, 255), cv2.FILLED)



    # отображаем видеопоток
    cv2.imshow('video', img)

    # клавиша для выхода
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
