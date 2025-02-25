import cv2
import numpy as np

cv2.namedWindow('HSV') # окно настроек HSV
cv2.namedWindow('Result') # окно с изображением

def callback(*arg):
    pass

cv2.createTrackbar('h1', 'HSV', 0, 255, callback)
cv2.createTrackbar('s1', 'HSV', 0, 255, callback)
cv2.createTrackbar('v1', 'HSV', 0, 255, callback)
cv2.createTrackbar('h2', 'HSV', 255, 255, callback)
cv2.createTrackbar('s2', 'HSV', 255, 255, callback)
cv2.createTrackbar('v2', 'HSV', 255, 255, callback)

img = cv2.imread('C:/Users/Vysochanskiy_mv/Desktop/Python/CV2/dog.jpg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
color = (0,0,255)
text = 'Red'

while True:
      # Записываем значения бегунков в переменные
      h1 = cv2.getTrackbarPos('h1', 'HSV')
      s1 = cv2.getTrackbarPos('s1', 'HSV')
      v1 = cv2.getTrackbarPos('v1', 'HSV')
      h2 = cv2.getTrackbarPos('h2', 'HSV')
      s2 = cv2.getTrackbarPos('s2', 'HSV')
      v2 = cv2.getTrackbarPos('v2', 'HSV')

      # Формируем начальный и конечный цвета фильтра
      hsv_min = np.array((h1, s1, v1), np.uint8)
      hsv_max = np.array((h2, s2, v2), np.uint8)

      # Применим цветовой фильтр к изображению
      filter_color = cv2.inRange(hsv, hsv_min, hsv_max)

      # Отобразим во втором окне результат
      cv2.imshow('Result', filter_color)
      
      # Когда результат во втором окне нас устоит, нажимаем Esc
      # Полученный цветовой фильтр сохраниться в переменную filter_color
      if cv2.waitKey(1) == 27:
          break
      

con, hir = cv2.findContours(filter_color, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for c in con:
    p = cv2.arcLength(c, True) # считаем длину контура
        
    if p > 1100: # если больше 1100 px
        cv2.drawContours(img, [c], -1, color, 5) # рисуем контур
        
        x, y = c[0][0][0], c[0][0][1] # создим координаты для точки
        cv2.circle(img, (x,y), 10, color, -1) # рисуем точку
        cv2.putText(img, text, (x-10, y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv2.LINE_AA) # подписываем цвет

        cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()