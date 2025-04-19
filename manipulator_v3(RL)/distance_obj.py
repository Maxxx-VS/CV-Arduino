import cv2
import numpy as np


def nothing(x):
    pass


# Калибровочные параметры (настройте под вашу камеру!)
REF_DISTANCE = 270  # Эталонное расстояние в мм
REF_AREA = 15000  # Площадь объекта в пикселях на эталонном расстоянии
MM_PER_PIXEL_AT_REF = 0.2  # Коэффициент мм/пиксель при REF_DISTANCE

cv2.namedWindow('HSV Threshold')
cv2.createTrackbar('H Min', 'HSV Threshold', 0, 179, nothing)
cv2.createTrackbar('H Max', 'HSV Threshold', 179, 179, nothing)
cv2.createTrackbar('S Min', 'HSV Threshold', 0, 255, nothing)
cv2.createTrackbar('S Max', 'HSV Threshold', 255, 255, nothing)
cv2.createTrackbar('V Min', 'HSV Threshold', 0, 255, nothing)
cv2.createTrackbar('V Max', 'HSV Threshold', 255, 255, nothing)

cap = cv2.VideoCapture(0)
min_object_size = 500


def calculate_distance(current_area):
    """Вычисляет расстояние до объекта в мм"""
    if current_area == 0: return 0
    return REF_DISTANCE * np.sqrt(REF_AREA / current_area)


def pixels_to_mm(pixels, current_distance):
    """Переводит пиксели в миллиметры с учетом текущего расстояния"""
    return pixels * MM_PER_PIXEL_AT_REF * (current_distance / REF_DISTANCE)


while True:
    ret, frame = cap.read()
    if not ret: break

    h, w = frame.shape[:2]
    cx, cy = w // 2, h // 2
    cv2.drawMarker(frame, (cx, cy), (0, 0, 255), cv2.MARKER_CROSS, 20, 2)

    # Обработка изображения
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([cv2.getTrackbarPos(f'{c} Min', 'HSV Threshold') for c in ['H', 'S', 'V']])
    upper = np.array([cv2.getTrackbarPos(f'{c} Max', 'HSV Threshold') for c in ['H', 'S', 'V']])

    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)

        if area > min_object_size:
            x, y, w, h = cv2.boundingRect(largest)
            obj_x, obj_y = x + w // 2, y + h // 2

            # Вычисление расстояний
            distance_z = calculate_distance(area)
            delta_x_px = obj_x - cx  # + справа, - слева
            delta_y_px = cy - obj_y  # + сверху, - снизу

            # Перевод в миллиметры
            delta_x_mm = pixels_to_mm(delta_x_px, distance_z)
            delta_y_mm = pixels_to_mm(delta_y_px, distance_z)

            # Отрисовка элементов
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.line(frame, (cx, cy), (obj_x, obj_y), (0, 255, 255), 2)
            cv2.circle(frame, (obj_x, obj_y), 5, (0, 255, 255), -1)

            # Вывод информации
            info = [
                f"X: {delta_x_mm:+.1f} mm",
                f"Y: {delta_y_mm:+.1f} mm",
                f"Distance: {distance_z:.1f} mm",
                f"Area: {area} px"
            ]
            for i, text in enumerate(info):
                cv2.putText(frame, text, (10, 30 + 30 * i),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Вывод в консоль
            print(f"X: {delta_x_mm:+.1f} mm | Y: {delta_y_mm:+.1f} mm | Distance: {distance_z:.1f} mm")
        else:
            print("Объект слишком мал")
    else:
        print("Объект не обнаружен")

    cv2.imshow('Tracking', frame)
    cv2.imshow('Mask', mask)

    if cv2.waitKey(1) == ord('q'): break

cap.release()
cv2.destroyAllWindows()