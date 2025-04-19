#include <Servo.h>

// Servo configuration
Servo servoY;   // Y-axis rotation (pin 10)
Servo servoA;   // Pin 9
Servo servoB;   // Pin 7
Servo servoC;         // Pin 8

// Current positions
float currentY = 90;
float currentA = 90;
float currentB = 90;
float currentC = 90;

// Target positions
float targetY = 90;
float targetA = 90;
float targetB = 90;
float targetC = 90;

void setup() {
  Serial.begin(9600);
  servoY.attach(10);
  servoA.attach(9);
  servoB.attach(7);
  servoC.attach(8);

  // Initial position
  updateServos();
  delay(1000);
}

void loop() {
  if (Serial.available() > 0) {
    String cmd = Serial.readStringUntil('\n');
    parseCommand(cmd);

    // Smooth movement
    while (abs(targetY - currentY) > 1 ||
           abs(targetA - currentA) > 1 ||
           abs(targetB - currentB) > 1 ||
           abs(targetC - currentC) > 1) {
      currentY += (targetY - currentY) * 0.1;
      currentA += (targetA - currentA) * 0.1;
      currentB += (targetB - currentB) * 0.1;
      currentC += (targetC - currentC) * 0.1;
      updateServos();
      delay(20);
    }

    Serial.println("READY");
  }
}

void parseCommand(String cmd) {
  // Example command: "X0.25 Y-0.10"
  int xIndex = cmd.indexOf("X");
  int yIndex = cmd.indexOf("Y");

  if (xIndex != -1 && yIndex != -1) {
    float xVal = cmd.substring(xIndex+1, yIndex).toFloat();
    float yVal = cmd.substring(yIndex+1).toFloat();

    // Convert normalized values to servo angles (example mapping)
    targetY = constrain(90 + yVal * 30, 0, 180);  // ±30° range

    // For pins 7/9 (opposite to 8)
    targetA = constrain(90 - xVal * 30, 0, 180);
    targetB = constrain(90 - xVal * 30, 0, 180);
    targetC = constrain(90 + xVal * 30, 0, 180);
  }
}

void updateServos() {
  servoY.write(currentY);
  servoA.write(currentA);
  servoB.write(currentB);
  servoC.write(currentC);
}