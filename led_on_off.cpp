const int ledPin = 13; // Пин, к которому подключен светодиод

void setup() {
  pinMode(ledPin, OUTPUT); // Устанавливаем пин как выход
  Serial.begin(9600);      // Запускаем последовательную связь
}

void loop() {
  if (Serial.available()) { // Если есть доступные данные
    char command = Serial.read(); // Читаем символ

    switch (command) {
      case 'H': // Команда включить светодиод
        digitalWrite(ledPin, HIGH);
        break;
      case 'L': // Команда выключить светодиод
        digitalWrite(ledPin, LOW);
        break;
    }
  }
}



// const int ledPin = 13; // Пин, к которому подключен светодиод
#include <Servo.h> // подключаем библиотеку для работы с сервоприводом
Servo servo1; // объявляем переменную servo типа "servo1"

void setup() {
  servo1.attach(11); // привязываем сервопривод к аналоговому выходу 11
  // pinMode(ledPin, OUTPUT); // Устанавливаем пин как выход
  Serial.begin(9600);      // Запускаем последовательную связь
}

void loop() {
  if (Serial.available()) { // Если есть доступные данные
    char command = Serial.read(); // Читаем символ

    switch (command) {
      case 'H': // Команда включить светодиод
        servo1.write(30); // ставим угол поворота под 0
         delay(2000); // ждем 2 секунды

        //  digitalWrite(ledPin, HIGH);
        //  break;

      case 'L': // Команда выключить светодиод
        servo1.write(90); // ставим угол поворота под 180
        delay(2000); // ждем 2 секунды
        // digitalWrite(ledPin, LOW);
        // break;
    }
  }
}