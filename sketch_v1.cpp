#include <Servo.h>                                                // Подключаем библиотеку для работы с серво
#include "Wire.h"                                                 // Библиотеки для работы с OLED экраном Arduino IDE
#include "Adafruit_GFX.h"
#include "Adafruit_SSD1306.h"

Adafruit_SSD1306 display(128, 64, &Wire, 4);                      // указываем размер экрана в пикселях

const int trigPin = 11;                                           // Пины подключения датчика HC-SR04
const int echoPin = 12;

Servo servo180;                                                   // Создаем объект «сервопривод» на 180 град
Servo servo360;                                                   // Создаем объект «сервопривод» на 360 град

void setup() {

  Serial.begin(9600);                                             // Запускаем последовательную связь

  servo180.attach(10);                                            // пин для подключения серво на 180 градусов
  servo360.attach(9);                                             // пин для подключения серво на 360 градусов
  servo180.write(15);                                              // начальная позиция серво 180 при запуске

  pinMode(trigPin, OUTPUT);                                       // настройка пина TRIG как выход
  pinMode(echoPin, INPUT);                                        // настройка пина ECHO как вход

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {               // адрес I2C может отличаться, проверьте!
    Serial.println(F("SSD1306 allocation failed"));
    for (;;);                                                     // если дисплей не инициализировался, зацикливаемся
  }

  display.clearDisplay();                                         // очистка буфера дисплея
}

void loop() {
  long duration, distance;

  digitalWrite(trigPin, LOW);                                     // очищаем сигнал TRIG
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);                                    // запуск измерения
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);                              // считываем длительность сигнала ECHO
  distance = duration * 0.034 / 2;                                // вычисляем расстояние

  //  Serial.print("Distance: ");
  //  Serial.println(distance);

  display.clearDisplay();
  display.setTextSize(2);                                         // устанавливаем размер текста
  display.setTextColor(WHITE);                                    // белый текст
  display.setCursor(0, 0);                                        // устанавливаем курсор
  display.print("Dist:");
  display.setCursor(104, 0);
  display.print("cm");
  display.setCursor(70, 0);
  display.print(distance);
  display.display();                                               // выводим содержимое буфера на экран
  delay(100);                                                      // небольшая задержка перед следующим измерением

  if (distance < 10) {

    Serial.println("Go_photo");                                   // отправляем команду для фото

  }

  if (Serial.available()) {                                       // Если есть доступные данные
    char command = Serial.read();

    if (command == 'R') {
      display.setTextSize(2.5);                                   // устанавливаем размер текста
      display.setCursor(10, 40);
      display.print("DETECTED!");
      display.display();                                          // выводим содержимое буфера на экран

      servo360.write(45);                                         // движение мотора против часовой стрелки
      delay(700);                                                 // ждем
      servo360.write(90);                                         // остановка сервопривода
      delay(1000);                                                // ждем

      servo180.write(40);                                         // ставим угол при сжатии (чембольше тем сильнее)
      delay(500);                                                 // ждем

      servo360.write(135);                                        // движение мотора по часовой стрелке
      delay(740);                                                 // ждем
      servo360.write(90);                                         // остановка сервопривода
      delay(1000);                                                // ждем

      servo180.write(20);                                         // команда ОТПУСТИТЬ ГРУЗ

    }
  }
}