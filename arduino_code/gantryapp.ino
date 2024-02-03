#include "gantry.h"
#include "SerialTransfer.h"

// SerialTransfer myTransfer;

void setup() {
  Serial.begin(115200);
  // myTransfer.begin(Serial);
  pinMode(30, OUTPUT);
  // initSystem();
  // goHome();
}


void loop() {
  uint16_t sendSize = 0;
  uint16_t recSize = 0;


  static float distX, distY, distZ, endd, end_servo;
  // int com;
  bool oneByOne = false;

  //  if (Serial.available() > 0) {
  if (Serial.available() > 0) {
    char input[128];                                   // Assuming a reasonable buffer size
    Serial.readBytesUntil(';', input, sizeof(input));  // Read until the semicolon (;)
    input[sizeof(input) - 1] = '\0';                   // Null-terminate the string



    char* token = strtok(input, " ");
    if (token != NULL) {
      distX = atof(token);

      token = strtok(NULL, " ");
      if (token != NULL) {
        distY = atof(token);

        token = strtok(NULL, " ");
        if (token != NULL) {
          distZ = atof(token);

          token = strtok(NULL, " ");
          if (token != NULL) {
            endd = atof(token);

            token = strtok(NULL, " ");
            if (token != NULL) {
              end_servo = atof(token);

              Serial.print("X: ");
              Serial.print(distX);
              Serial.print(", Y: ");
              Serial.print(distY);
              Serial.print(", Z: ");
              Serial.println(distZ);
              Serial.print(", Servo: ");
              Serial.println(end_servo);


              if (distX == -1 && distY == -1 && distZ == -1 && endd == 2) {
                initSystem();
                goHome();
              }
              if (distX == -1 && distY == -1 && distZ == -1 && endd == 5) {
                digitalWrite(40, HIGH);
                goToXYZ(600, 500, 0, oneByOne);
                goToXYZ(0, 0, 0, oneByOne);
              }
              if (distX == -1 && distY == -1 && distZ == -1 && endd == 6) {
                digitalWrite(40, HIGH);
              }
              if (distX == -1 && distY == -1 && distZ == -1 && endd == 3) {
                digitalWrite(40, LOW);
              }
              if (distX == -1 && distY == -1 && distZ == -1) {
                if (endd == 0) {
                  gripperClose(0);
                } else if (endd == 1) {
                  gripperClose(18);
                }
              }
              if (distX == -1 && distY == -1 && distZ == -1) {
                if (endd == 9) {
                  end_servo_rot(end_servo);
                  Serial.println("r");
                }
              } else {
                //  goTozXY(distX,distY,distZ);
                goToXYZ(distX, distY, distZ, oneByOne);
                if (endd == 0) {
                  gripperClose(0);
                } else if (endd == 1) {
                  gripperClose(18);
                }
                end_servo_rot(end_servo);
              }
            }
          }
        }
      }
    }
  }
}
