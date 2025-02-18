import cv2
import serial
from time import sleep

# Настройка последовательного порта
ser = serial.Serial('/dev/ttyUSB0', 9600)

def send_command(command):
    ser.write(bytes(command + '\n', 'utf-8'))

def take_photo(): # Функция для активации камеры (сделать фото)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Не удалось инициализировать камеру")
        return

    ret, frame = cap.read()
    if not ret:
        print("Не удалось сделать снимок")
        return

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # переводим BGR в HSV
    binary = cv2.inRange(hsv, (30, 50, 70), (60, 255, 255)) # пороговая обработка кадра
    con, _ = cv2.findContours(binary,
                              cv2.RETR_EXTERNAL,
                              cv2.CHAIN_APPROX_NONE)  # получаем контуры объектов
    if len(con) != 0:  # если нашли хоть 1 контур
        max_con = max(con, key=cv2.contourArea)  # выбираем самый большой
        moments = cv2.moments(max_con)  # получаем моменты контура

        if moments["m00"] > 500:
            print("YES")
            cv2.imwrite('../img/photo.jpg', binary)
            cap.release()
            print("Фото сохранено в файл 'photo.jpg'")
            send_command('R')
            sleep(4)


while True: # Считываем данные из последовательного порта (команда для фото)
    data = ser.readline().decode().strip()
    if data == "Go_photo": # Получает от Arduino команду на фото
        take_photo()





