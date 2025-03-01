#include <Servo.h>                                                // подключаем библиотеку для работы с серво
#include "Wire.h"                                                 // библиотеки для работы с OLED экраном Arduino IDE
#include "Adafruit_GFX.h"
#include "Adafruit_SSD1306.h"

Adafruit_SSD1306 display(128, 64, &Wire, 4);                      // указываем размер экрана в пикселях

Servo servo180;                                                   // создаем объект «сервопривод» на 180 град
Servo servo360;                                                   // создаем объект «сервопривод» на 360 град

void setup() {

  Serial.begin(9600);                                             // запускаем последовательную связь

  servo180.attach(10);                                            // пин для подключения серво на 180 градусов
  servo360.attach(9);                                             // пин для подключения серво на 360 градусов
  servo180.write(15);                                             // начальная позиция серво 180 при запуске

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {               // адрес I2C может отличаться, проверьте!
    Serial.println(F("SSD1306 allocation failed"));
    for (;;);                                                     // если дисплей не инициализировался, зацикливаемся
  }
}

void loop() {
  display.setTextColor(WHITE);                                    // устанавливаем белый текст
  display.setTextSize(2);                                         // устанавливаем размер текста

  display.clearDisplay();                                         // очищаем дисплей
  display.setCursor(5, 25);                                       // устанавливаем точку начала вывода текста
  display.print("WORKING");                                       // текст для вывода
  display.display();                                              // выводим содержимое буфера на экран
  delay(500);                                                     // небольшая задержка перед следующим измерением

  display.clearDisplay();
  display.setCursor(5, 25);
  display.print("WORKING...");
  display.display();
  delay(500);

  if (Serial.available()) {                                       // если есть доступные данные
    char command = Serial.read();                                 // считываем команду на захват
    String input = Serial.readString();                           // считываем название объекта

    if (command == 'R') {
      display.clearDisplay();

      display.setTextSize(2.5);
      display.setCursor(10, 0);
      display.print("DETECTED!");
      display.display();

      display.setTextSize(3.5);
      display.setCursor(0, 5);
      display.print(input);
      display.display();

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