import mediapipe as mp
import cv2



camera = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

p = [0 for i in range(21)]
finger = [0 for i in range(5)]

def distance(point1, point2):
    return abs(point1 - point2)

while True:
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

            # условие соприкосновения пальцев (место для полета фантазии)
            if distance(p[8], p[4]) <= 20:
                print("Касание!")

    # отображаем видеопоток
    cv2.imshow('video', img)

    # клавиша для выхода
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()