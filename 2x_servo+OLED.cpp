#include <Servo.h>                                  // Подключаем библиотеку для работы с сервоприводом


#include "Wire.h"                                   // библиотеки для работы с OLED экраном Arduino IDE
#include "Adafruit_GFX.h"
#include "Adafruit_SSD1306.h"

Adafruit_SSD1306 display(128, 64, &Wire, 4);        // указываем размер экрана в пикселях
Servo servo180;                                     // Создаем объект типа «сервопривод» на 180 градусов
Servo servo360;                                     // Создаем объект типа «сервопривод» на 360 градусов


void setup() {

  Serial.begin(9600);                               // Запускаем последовательную связь

  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);        // указываем адрес устройства на шине
  display.clearDisplay();                           // очищаем экран
  display.setTextSize(1, 2);                        // указываем размер шрифта
  display.setTextColor(SSD1306_WHITE);              // указываем цвет надписи

  display.setCursor(20, 10);
  display.println("ARDUINO");
  display.display();
  delay(2000);
  display.clearDisplay();                           // очищаем экран


  servo180.attach(11);                              // пин для подключения серво на 180 градусов
  servo360.attach(9);                               // пин для подключения серво на 360 градусов
  servo180.write(0);                                // начальная позиция серво 180 при запуске
//  servo360.write(0);                              // начальная позиция серво 360 при запуске

}

void loop() {

  display.setTextSize(3);                           // указываем размер шрифта
  display.setTextColor(SSD1306_WHITE);              // указываем цвет надписи


  display.setCursor(0, 10);                         // (отступ слева, отступ сверху)
  display.println("TARANIN");
  display.display();
  delay(100);
  display.clearDisplay();                           // очищаем экран

  if (Serial.available()) {                         // Если есть доступные данные
    char command = Serial.read();                   // Читаем символ

    switch (command) {
      case 'H':                                     // команда ОТПУСТИТЬ ГРУЗ
        servo180.write(20);                         // ставим угол поворота под 0
        delay(1000);                                // ждем

        servo360.write(45);                         // движение мотора против часовой стрелки
        delay(850);                                 // ждем
        servo360.write(90);                         // остановка сервопривода
        delay(850);                                 // ждем
        break;


      case 'L':                                     // команда ВЗЯТЬ ГРУЗ
        servo180.write(45);                         // ставим угол поворота
        delay(1000);                                // ждем

        servo360.write(135);                        // движение мотора по часовой стрелке
        delay(910);                                 // ждем
        servo360.write(90);                         // остановка сервопривода
        delay(910);                                 // ждем
        break;


    }
  }
}