import cv2
import numpy as np


def measure_distance_from_center(image_path):
    # Загрузка изображения
    image = cv2.imread(image_path)
    if image is None:
        print("Не удалось загрузить изображение")
        return

    # Преобразование в оттенки серого
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Применение порогового значения для выделения объекта
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Нахождение контуров
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print("Объекты не найдены")
        return

    # Выбираем самый большой контур (предполагая, что это наш объект)
    largest_contour = max(contours, key=cv2.contourArea)

    # Находим центр масс объекта (центроид)
    M = cv2.moments(largest_contour)
    if M["m00"] == 0:
        print("Не удалось вычислить моменты контура")
        return

    cx_object = int(M["m10"] / M["m00"])
    cy_object = int(M["m01"] / M["m00"])

    # Находим центр изображения
    h, w = image.shape[:2]
    cx_image = w // 2
    cy_image = h // 2

    # Вычисляем расстояние между центрами
    distance = np.sqrt((cx_object - cx_image) ** 2 + (cy_object - cy_image) ** 2)

    # Рисуем центры и линию между ними для визуализации
    cv2.circle(image, (cx_image, cy_image), 5, (0, 0, 255), -1)  # Центр изображения (красный)
    cv2.circle(image, (cx_object, cy_object), 5, (0, 255, 0), -1)  # Центр объекта (зеленый)
    cv2.line(image, (cx_image, cy_image), (cx_object, cy_object), (255, 0, 0), 2)  # Линия (синяя)

    # Выводим расстояние на изображение
    cv2.putText(image, f"Distance: {distance:.2f} px", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Показываем результат
    cv2.imshow("Distance Measurement", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return distance


# Пример использования
image_path = "img/111.jpeg"  # Укажите путь к вашему изображению
distance = measure_distance_from_center(image_path)
print(f"Расстояние от центра до объекта: {distance} пикселей")