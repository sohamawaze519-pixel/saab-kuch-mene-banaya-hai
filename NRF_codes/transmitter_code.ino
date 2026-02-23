#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(7, 8);   // CE, CSN
const byte address[6] = "00001";

struct Data_Package {
  int xAxis;
  int yAxis;
};

Data_Package data;

// Smooth joystick reading
int readJoystick(int pin) {
  int sum = 0;
  for (int i = 0; i < 5; i++) {
    sum += analogRead(pin);
    delayMicroseconds(200);
  }
  return sum / 5;
}

void setup() {
  Serial.begin(9600);

  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_LOW);
  radio.stopListening();

  Serial.println("TX Ready");
}

void loop() {

  // Read joystick smoothly
  data.xAxis = readJoystick(A0);   // Forward/Backward
  data.yAxis = readJoystick(A1);   // Left/Right

  // Safety check (avoid garbage)
  if (data.xAxis < 0 || data.xAxis > 1023 ||
      data.yAxis < 0 || data.yAxis > 1023) {
    return;
  }

  // Send data
  bool success = radio.write(&data, sizeof(data));

  Serial.print("X: ");
  Serial.print(data.xAxis);
  Serial.print("  Y: ");
  Serial.print(data.yAxis);

  if (success) {
    Serial.println("  Sent");
  } else {
    Serial.println("  Failed");
  }

  delay(20);   // smooth transmission
}