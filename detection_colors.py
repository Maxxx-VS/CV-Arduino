import cv2
import time

def cam():
    camera = cv2.VideoCapture(0)
    i_see = False  # флаг нахождения контура

    while True:
            success, frame = camera.read()

            if success:                                              # если прочитали успешно
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)         # переводим BGR в HSV
                binary = cv2.inRange(hsv, (30, 50, 70), (60, 255, 255))          # пороговая обработка кадра

                con, _ = cv2.findContours(binary,
                                                  cv2.RETR_EXTERNAL,
                                                  cv2.CHAIN_APPROX_NONE)  # получаем контуры объектов

                if len(con) != 0:                                     # если нашли хоть 1 контур
                    max_con = max(con, key=cv2.contourArea)           # выбираем самый большой
                    moments = cv2.moments(max_con)                    # получаем моменты контура

                    if moments["m00"] > 500:                           # площадь контура px

                        cx = int(moments["m10"] / moments["m00"])     # центр контура по x
                        cy = int(moments["m10"] / moments["m00"])     # центр контура по y

                        i_see = True                                # меняем флаг, если нашли контур
                        print("yes")
                        continue

                    cv2.imshow('Video', binary)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    camera.release()
    cv2.destroyAllWindows()

cam()