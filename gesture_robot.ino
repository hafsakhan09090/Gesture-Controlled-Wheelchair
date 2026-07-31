// Arduino firmware for a hand-gesture controlled two-wheel robot.

// Motor A (left motor)
#define ENA 5
#define IN1 6
#define IN2 7

// Motor B (right motor)
#define ENB 10
#define IN3 8
#define IN4 9

// Optional LEDs or buzzer
#define LED1 2
#define LED2 3

const int MOTOR_SPEED = 200;

void setup() {
  Serial.begin(9600);

  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);

  stopMotors();
  digitalWrite(LED1, LOW);
  digitalWrite(LED2, LOW);

  Serial.println("Ready: 0 Stop | 1 Forward | 2 Backward | 3 Right | 4 Left | 5 Honk");
}

void loop() {
  if (!Serial.available()) {
    return;
  }

  const char command = Serial.read();

  switch (command) {
    case '0': stopMotors(); break;
    case '1': moveForward(); break;
    case '2': moveBackward(); break;
    case '3': turnRight(); break;
    case '4': turnLeft(); break;
    case '5': honk(); break;
    case '6': digitalWrite(LED2, HIGH); break;
    default: Serial.println("Invalid command"); break;
  }
}

void moveForward() {
  setMotors(HIGH, LOW, HIGH, LOW);
  Serial.println("Moving forward");
}

void moveBackward() {
  setMotors(LOW, HIGH, LOW, HIGH);
  Serial.println("Moving backward");
}

void turnRight() {
  setMotors(HIGH, LOW, LOW, HIGH);
  Serial.println("Turning right");
}

void turnLeft() {
  setMotors(LOW, HIGH, HIGH, LOW);
  Serial.println("Turning left");
}

void stopMotors() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
  Serial.println("Motors stopped");
}

void setMotors(int leftForward, int leftBackward, int rightForward, int rightBackward) {
  digitalWrite(IN1, leftForward);
  digitalWrite(IN2, leftBackward);
  digitalWrite(IN3, rightForward);
  digitalWrite(IN4, rightBackward);
  analogWrite(ENA, MOTOR_SPEED);
  analogWrite(ENB, MOTOR_SPEED);
}

void honk() {
  // Two short pulses. Commands received during this short sequence wait in the buffer.
  for (int i = 0; i < 2; i++) {
    digitalWrite(LED1, HIGH);
    delay(300);
    digitalWrite(LED1, LOW);
    delay(300);
  }
}
