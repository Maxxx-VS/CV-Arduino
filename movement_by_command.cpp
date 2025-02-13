#include <Servo.h> // подключаем библиотеку для работы с сервоприводом
Servo servo1; // объявляем переменную servo типа "servo1"

void setup() {
  servo1.attach(11); // привязываем сервопривод к аналоговому выходу 11
  // pinMode(ledPin, OUTPUT); // Устанавливаем пин как выход
  Serial.begin(9600);      // Запускаем последовательную связь
  servo1.write(0); // начальная позиция серво при запуске
}

void loop() {
  if (Serial.available()) { // Если есть доступные данные
    char command = Serial.read(); // Читаем символ

    switch (command) {
      case 'H': // Команда включить светодиод
        servo1.write(0); // ставим угол поворота под 0
         delay(1000); // ждем 1 секунду
         break;


      case 'L': // Команда выключить светодиод
        servo1.write(45); // ставим угол поворота
        delay(1000); // ждем 1 секунду
        break;

    }
  }
}