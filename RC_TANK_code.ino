// Motor control pins
int LMP = 8;  // Left Motor Positive
int LMN = 9;  // Left Motor Negative
int RMP = 6;  // Right Motor Positive
int RMN = 7;  // Right Motor Negative

void setup() {
  // Set motor control pins as OUTPUT
  pinMode(LMP, OUTPUT);
  pinMode(LMN, OUTPUT);
  pinMode(RMP, OUTPUT);
  pinMode(RMN, OUTPUT);
  
  // Start serial communication
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    char Direction = Serial.read(); // Read a single character

    switch (Direction) {
      case 'F': // Move Forward (do as per your applications commands(all directions))
        digitalWrite(LMP, HIGH);
        digitalWrite(LMN, LOW);
        digitalWrite(RMP, HIGH);
        digitalWrite(RMN, LOW);
        break;

      case 'B': // Move Backward
        digitalWrite(LMP, LOW);
        digitalWrite(LMN, HIGH);
        digitalWrite(RMP, LOW);
        digitalWrite(RMN, HIGH);
        break;

      case 'R': // Turn Left
        digitalWrite(LMP, LOW);
        digitalWrite(LMN, HIGH);
        digitalWrite(RMP, HIGH);
        digitalWrite(RMN, LOW);
        break;

      case 'L': // Turn Right
        digitalWrite(LMP, HIGH);
        digitalWrite(LMN, LOW);
        digitalWrite(RMP, LOW);
        digitalWrite(RMN, HIGH);
        break;

      case 'S': // Stop
        digitalWrite(LMP, LOW);
        digitalWrite(LMN, LOW);
        digitalWrite(RMP, LOW);
        digitalWrite(RMN, LOW);
        break;
    }
  }
}
