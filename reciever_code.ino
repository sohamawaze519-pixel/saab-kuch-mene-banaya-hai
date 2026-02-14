#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(7, 8);
const byte address[6] = "00001";

struct Data_Package {
  int xAxis;
  int yAxis;
};

Data_Package data;

// L298N pins
#define IN1 2
#define IN2 3
#define IN3 4
#define IN4 5

#define CENTER 512
#define DEADZONE 50

unsigned long lastSignalTime = 0;

void stopCar() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

void setup() {
  Serial.begin(9600);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  stopCar();

  radio.begin();
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_LOW);
  radio.startListening();

  Serial.println("RX Ready");
}

void loop() {

  if (radio.available()) {
    radio.read(&data, sizeof(data));
    lastSignalTime = millis();
  }

  // 🔴 FAILSAFE
  if (millis() - lastSignalTime > 400) {
    stopCar();
    return;
  }

  int x = data.xAxis;
  int y = data.yAxis;

  Serial.print("X: ");
  Serial.print(x);
  Serial.print(" Y: ");
  Serial.println(y);

  // FORWARD
  if (y > CENTER + DEADZONE) {
    forward();
  }
  // BACKWARD
  else if (y < CENTER - DEADZONE) {
    backward();
  }
  // RIGHT
  else if (x > CENTER + DEADZONE) {
    right();
  }
  // LEFT
  else if (x < CENTER - DEADZONE) {
    left();
  }
  // STOP
  else {
    stopCar();
  }
}

void forward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void backward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void left() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void right() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

