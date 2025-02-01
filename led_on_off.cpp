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
