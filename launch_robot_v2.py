import cv2
import serial
from time import sleep
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
import os

# Загрузка обученной модели
model = load_model('/home/max/PycharmProjects/CV+Arduino/MODELS/cifar10_model.keras')
# Классы CIFAR-10
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
# Настройка последовательного порта
ser = serial.Serial('/dev/ttyUSB0', 9600)

# Функция для передачи на Arduino команды захвата объекта
def send_command(command):
    ser.write(bytes(command + '\n', 'utf-8'))

# Функция для передачи на OLED предсказанного класса
def send_string(string_to_send):
    ser.write(string_to_send.encode())

# Функция для активации камеры (сделать фото)
def take_photo():

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Не удалось инициализировать камеру")
        return

    ret, frame = cap.read()
    if not ret:
        print("Не удалось сделать снимок")
        return

    cv2.imwrite('../img/photo.jpg', frame)   # Делаем фото с камеры
    cap.release()                                    # Освобождаем ресурс камеры

    img_cut = cv2.imread('../img/photo.jpg')         # Загружаем для обрезания фото
    x, y, w, h = 250, 75, 200, 200                      # Координаты для обрезания фото
    roi = img_cut[y:y + h, x:x + w]                  # Выделение области по координатам
    cv2.imwrite('../img/photo.jpg', roi)     # Сохраняем обрезанное фото
    cap.release()                                    # Освобождаем ресурс камеры
    print("Фото сохранено в файл 'photo.jpg'")

    img = image.load_img('../img/photo.jpg', target_size=(32, 32))   # Загрузка изображения и изменение размера до 32x32
    img_array = image.img_to_array(img)                              # Преобразование изображения в массив numpy
    img_array = img_array / 255.0                                    # Нормализация изображения (приведение к диапазону [0, 1])
    img_array = np.expand_dims(img_array, axis=0)                    # Добавление размерности батча (модель ожидает вход с формой (None, 32, 32, 3))

    # Предсказание класса
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions)

    # Вывод результата
    print(f"Предсказанный класс: {class_names[predicted_class]}")
    print(f"Вероятности по классам: {predictions}")
    sleep(3)                # Задержка между детекцией

    if class_names[predicted_class] != 'cat':
        sleep(0.5)                                     # Задержка перед захватом
        send_command('R')
        string_to_send = str(class_names[predicted_class]).upper()
        send_string(string_to_send + "\n")

        # Визуализация изображения
        plt.imshow(image.load_img('../img/photo.jpg'))
        plt.title(f"Предсказанный класс: {class_names[predicted_class]}")
        plt.axis('off')
        plt.show(block=False)
        plt.pause(3)
        plt.close()

# Считываем данные из последовательного порта (команда для фото)
while True:
    take_photo()





