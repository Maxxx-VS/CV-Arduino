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

    cv2.imwrite('../img/photo.jpg', frame)
    cap.release()
    print("Фото сохранено в файл 'photo.jpg'")

    img = image.load_img('../img/photo.jpg', target_size=(32, 32))   # Загрузка изображения и изменение размера до 32x32
    img_array = image.img_to_array(img)   # Преобразование изображения в массив numpy
    img_array = img_array / 255.0   # Нормализация изображения (приведение к диапазону [0, 1])
    img_array = np.expand_dims(img_array, axis=0)   # Добавление размерности батча (модель ожидает вход с формой (None, 32, 32, 3))
    # Предсказание класса
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions)
    # Вывод результата
    print(f"Предсказанный класс: {class_names[predicted_class]}")
    print(f"Вероятности по классам: {predictions}")

    if class_names[predicted_class] == 'bird':
        send_command('R')
    # os.remove('../img/photo.jpg')
    # sleep()

    # Визуализация изображения
    plt.imshow(image.load_img('../img/photo.jpg'))
    plt.title(f"Предсказанный класс: {class_names[predicted_class]}")
    plt.axis('off')
    plt.show(block=False)
    plt.pause(3)
    plt.close()

# Считываем данные из последовательного порта (команда для фото)
while True:
    data = ser.readline().decode().strip()
    if data == "Go_photo": # Получает от Arduino команду на фото
        take_photo()





