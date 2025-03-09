#include <Servo.h>

// Создаем объект Servo для управления сервоприводом
Servo servo1;
Servo servo2;
Servo servo3;

void setup() {
  // Присоединяем сервопривод к пину 9 на плате Arduino
  servo1.attach(9);
  servo2.attach(10);
  servo3.attach(11);

  servo1.write(90);  // Устанавливаем сервопривод в начальное положение
  servo2.write(90);  // Устанавливаем сервопривод в начальное положение
  servo3.write(90);  // Устанавливаем сервопривод в начальное положение
}

void loop() {
  // Цикл для движения сервопривода от 0 до 180 градусов
  for (int angle = 0; angle <= 180; angle++) {
    servo1.write(angle);      // Устанавливаем угол
    servo2.write(angle);
    servo3.write(angle);
    delay(25);               // Задержка для плавного перемещения


  }

  // Цикл для обратного движения от 180 до 0 градусов
  for (int angle = 180; angle >= 0; angle--) {
    servo1.write(angle);
    servo2.write(angle);
    servo3.write(angle);
    delay(25);               // Задержка для плавного перемещения
  }
}