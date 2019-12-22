#include <AccelStepper.h>
#include <SoftwareSerial.h>
#define HALFSTEP 8  //Half-step mode (8 step control signal sequence)

// Motor pin definitions
#define mtrPin1  8     // IN1 on the ULN2003 driver 1
#define mtrPin2  9     // IN2 on the ULN2003 driver 1
#define mtrPin3  10     // IN3 on the ULN2003 driver 1
#define mtrPin4  11     // IN4 on the ULN2003 driver 1

#define mtrPin_1  4     // IN1 on the ULN2003 driver 2
#define mtrPin_2  5     // IN2 on the ULN2003 driver 2
#define mtrPin_3  6     // IN3 on the ULN2003 driver 2
#define mtrPin_4  7     // IN4 on the ULN2003 driver 2

AccelStepper stepper1(HALFSTEP, mtrPin1, mtrPin3, mtrPin2, mtrPin4);     // 약 조제에서 스텝모터지정
AccelStepper stepper2(HALFSTEP, mtrPin_1, mtrPin_3, mtrPin_2, mtrPin_4); // 약 조제에서 스텝모터지정

int speedLeft = 1500;
int speedRight = 1500;

int leftWheelForeward = 1;
int leftWheelBackward = -1;
int rightWheelForeward = -1;
int rightWheelBackward = 1;
char controlKey = 1;

void setup() {
  Serial.begin(9600);                    // 시리얼 포트 9600 지정
  stepper1.setMaxSpeed(2000.0);
  stepper2.setMaxSpeed(2000.0);
}

void loop() {
  while( Serial.available() > 0 ) {      // 시리얼 포트가 열려있는 동안
    char c = Serial.read();              // 시리얼 통신을 통해 들어오는 데이터 읽기
    if ( c == '1' ) {                    // '1'은 감기를 의미
      Serial.write(c);
      long n  = 116000;                  // 감기에 해당하는 약 조제를 위한 매개변수
      _Go(n);                            // 감기약 조제
    }    
    else if ( c == '2'){                 // '2'은 두통을 의미
      Serial.write(c);
      long n  = 220000;                  // 두통에 해당하는 약 조제를 위한 매개변수
      _Go(n);                            // 두통약 조제
    }

    // motor stop
    stepper1.stop(); //motor stop
    stepper2.stop();
    stepper1.disableOutputs(); //motor power disconnect, so motor led will turn off
    stepper2.disableOutputs();
  }
}

void _Go(long i) {  //foreward
  for (long j = 0; j<i; j++) {
    stepper1.move(leftWheelForeward);  // 방향은 1
    stepper2.move(rightWheelForeward); // 방향은 -1
    stepper1.setSpeed(1000);
    stepper2.setSpeed(1000);
    stepper1.runSpeedToPosition();
    stepper2.runSpeedToPosition();
  }
}
