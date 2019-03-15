#include "quaternionFilters.h"
#include "MPU9250.h"
#include <Wire.h>
#include <ESP8266WiFi.h>

#define MAX_SRV_CLIENTS 1
#define pot A0
#define btn1 D9
#define btn2 D10
#define clk D8
#define AB D0

String inputString;
#define PORT 8080
const char* ssid = "WiFiCar";
const char* password = "pass1234";

WiFiServer server(PORT);
WiFiClient serverClients[MAX_SRV_CLIENTS];

unsigned long previousMillis = 0, temp = 0;
const long interval = 200;


// Hardware setup:
// MPU9250 Breakout --------- Arduino
// VDD ---------------------- 3.3V
// VDDI --------------------- 3.3V
// SDA ----------------------- A4
// SCL ----------------------- A5
// GND ---------------------- GND

MPU9250 myIMU;

void setup() {
  Wire.begin(D2,D1);
  Serial.begin(115200);
  delay(100);
    
  IPAddress ip(192,168,43,204);
  IPAddress gateway(192,168,43,1);
  IPAddress subnet(255,255,255,0);

  WiFi.config(ip, gateway, subnet);

  WiFi.mode(WIFI_STA);

  WiFi.begin(ssid, password);
  Serial.println("Hola2");
  uint8_t i = 0;
  while (WiFi.status() != WL_CONNECTED && i++ < 20) delay(500);
  if (i == 21) {
    Serial.print("Could not connect to: "); Serial.println(ssid);
    while (true){
      Serial.print("Error");
      delay(500); }
  } else {
    Serial.println("It´s connected");
  }

  Serial.println("Trying to connect to MPU9250");  
  
  byte c = myIMU.readByte(MPU9250_ADDRESS, WHO_AM_I_MPU9250);
  if(c == 0x71)
  {
    Serial.println("\nMPU9250 is online...");
    myIMU.MPU9250SelfTest(myIMU.SelfTest);
    myIMU.calibrateMPU9250(myIMU.gyroBias, myIMU.accelBias);
    myIMU.initMPU9250();
    byte d = myIMU.readByte(AK8963_ADDRESS, WHO_AM_I_AK8963);
    // Get magnetometer calibration from AK8963 ROM
    myIMU.initAK8963(myIMU.magCalibration);
    //myIMU.magcalMPU9250(myIMU.magbias, myIMU.magscale);
    myIMU.magbias[0] = 384.34;
    myIMU.magbias[1] = 271.41;
    myIMU.magbias[2] = -592.14;
    myIMU.magscale[0] = 1.25;
    myIMU.magscale[1] = 1.12;
    myIMU.magscale[2] = 0.76;

    
  }
  else {
    Serial.print("Could not connect to MPU9250: 0x");
    Serial.println(c, HEX);
    while(true){
      Serial.println("Error MPU not working   ");
      delay(100); // Loop forever if communication doesn't happen
    }
  }
  
  server.begin();
  server.setNoDelay(true);

  pinMode(btn1, INPUT);
  pinMode(btn2, INPUT);
  pinMode(pot, INPUT);
  pinMode(clk,OUTPUT);
  pinMode(AB,OUTPUT);
  pinMode(D3,OUTPUT);
  pinMode(D4,OUTPUT);
  pinMode(D5,OUTPUT);
  pinMode(D6,OUTPUT);
  pinMode(D7,OUTPUT);
  
  
  delay(10);


}

void loop() {
  unsigned long currentMillis = millis();
  uint8_t i;
  //check if there are any new clients
  if (server.hasClient()) {
    for (i = 0; i < MAX_SRV_CLIENTS; i++) {
      //find free/disconnected spot
      if (!serverClients[i] || !serverClients[i].connected()) {
        if (serverClients[i]) serverClients[i].stop();
        serverClients[i] = server.available();
        continue;
      }
    }
    //no free/disconnected spot so reject
    WiFiClient serverClient = server.available();
    serverClient.stop();
  }

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    for (i = 0; i < MAX_SRV_CLIENTS; i++) {
      if (serverClients[i] && serverClients[i].connected()) {
        if(serverClients[i].available()){
          String message= serverClients[i].readStringUntil('\r');
          String respuesta;
          process(message, &respuesta);
          serverClients[i].println(respuesta);
        }  
      }
    }
  }
}

bool process(String input, String *respuesta){
  Serial.println("Processing...........");
  Serial.println(input);
  if(input == "read;\r"){
    *respuesta = leerDatos();
  }
  else{
    int comienzo=0, delComa, del2puntos;
    bool result=false;
    delComa= input.indexOf(':');
    while(delComa>0){
      String comando = input.substring(comienzo, delComa);
      Serial.print("processing comando:");
      del2puntos=comando.indexOf(':');
      if(del2puntos>0){
        String llave= comando.substring(0,del2puntos);
        String valor= comando.substring(del2puntos+1);
        Serial.print("Llave");
        Serial.println(llave);
        *respuesta = definir(llave,valor);
    }
    comienzo=delComa+1;
    delComa=input.indexOf(';',comienzo);
    } 
  }
}

String definir(String llave, String valor){
  
}

String leerDatos(){
    String message;
    readBtns(&message);
    readPot(&message);
    readMPU(&message);
    delay(50);
    message+=";";
    return message;
}

/**
 * Funcion para hacer print del display y los leds 
 */

 
void showValues(char leds[7],char num){
  shiftOut(AB, clk, LSBFIRST,num2Byte(num));
  for(int i = 0; i<6;i++){
    bool OnOff = false;
    if(leds[i]=='1'){OnOff = true;} 
    digitalWrite(i+2,OnOff);
  }
}

/**
 * Convertir un caracter de un numero en un digito para el display 7 segmentos
 * El ultimo bit siempre es en 1
 * Esta funcion solo sirve para displays de tipo catodo comun.
 */


byte num2Byte(char num){
  byte numBin=B11111111;
  switch (num){
   case '0':
            //abcdefg.
      numBin=B00000011;
      break;
   case '1':
            //abcdefg.
      numBin=B10011111;
      break;
   case '2':
           //abcdefg.
      numBin=B00100101;
      break;
   case '3':
      numBin=B00001101;
      break;
   case '4':
      numBin=B10011001;
      break;
   case '5':
      numBin=B01001001;
      break;
   case '6':
      numBin=B01000001;
      break;
   case '7':  
            //abcdefg.
      numBin=B00011111;
      break;
   case '8':
            //abcdefg.
      numBin=B00000001;
      break;
   case '9':
            //abcdefg.
      numBin=B00011001;
      break;
  }
  return numBin;
}



void readBtns(String *message){
  *message += "btn1=";
  if(digitalRead(btn1)){*message += "1";}
  else{*message += "0";}
  *message += ",btn2=";
  if(digitalRead(btn2)){*message += "1";}
  else{*message += "0";}
}

/**
 * Funcion para leer el potenciometro
 */


void readPot (String* mns){
  *mns += ",pot=";
  int value = analogRead(pot);
  value = map(value, 0, 1024, 0, 100);
  *mns += String(value);
}


void readMPU(String* mns){
  if (myIMU.readByte(MPU9250_ADDRESS, INT_STATUS) & 0x01)
  {  
    myIMU.readAccelData(myIMU.accelCount);  // Read the x/y/z adc values
    myIMU.getAres();

    // Now we'll calculate the accleration value into actual g's
    // This depends on scale being set
    myIMU.ax = (float)myIMU.accelCount[0]*myIMU.aRes; // - accelBias[0];
    myIMU.ay = (float)myIMU.accelCount[1]*myIMU.aRes; // - accelBias[1];
    myIMU.az = (float)myIMU.accelCount[2]*myIMU.aRes; // - accelBias[2];

    myIMU.readGyroData(myIMU.gyroCount);  // Read the x/y/z adc values
    myIMU.getGres();

    // Calculate the gyro value into actual degrees per second
    // This depends on scale being set
    myIMU.gx = (float)myIMU.gyroCount[0]*myIMU.gRes;
    myIMU.gy = (float)myIMU.gyroCount[1]*myIMU.gRes;
    myIMU.gz = (float)myIMU.gyroCount[2]*myIMU.gRes;

    myIMU.readMagData(myIMU.magCount);  // Read the x/y/z adc values
    myIMU.getMres();

    // Calculate the magnetometer values in milliGauss
    // Include factory calibration per data sheet and user environmental
    // corrections
    // Get actual magnetometer value, this depends on scale being set
    myIMU.mx = (float)myIMU.magCount[0]*myIMU.mRes*myIMU.magCalibration[0] - myIMU.magbias[0];
    myIMU.my = (float)myIMU.magCount[1]*myIMU.mRes*myIMU.magCalibration[1] - myIMU.magbias[1];
    myIMU.mz = (float)myIMU.magCount[2]*myIMU.mRes*myIMU.magCalibration[2] - myIMU.magbias[2];
    myIMU.mx *= myIMU.magscale[0];
    myIMU.my *= myIMU.magscale[1];
    myIMU.mz *= myIMU.magscale[2];
  } // if (readByte(MPU9250_ADDRESS, INT_STATUS) & 0x01)

  // Must be called before updating quaternions!
  myIMU.updateTime();

  // Sensors x (y)-axis of the accelerometer is aligned with the y (x)-axis of
  // the magnetometer; the magnetometer z-axis (+ down) is opposite to z-axis
  // (+ up) of accelerometer and gyro! We have to make some allowance for this
  // orientationmismatch in feeding the output to the quaternion filter. For the
  // MPU-9250, we have chosen a magnetic rotation that keeps the sensor forward
  // along the x-axis just like in the LSM9DS0 sensor. This rotation can be
  // modified to allow any convenient orientation convention. This is ok by
  // aircraft orientation standards! Pass gyro rate as rad/s
  //MadgwickQuaternionUpdate(ax, ay, az, gx*PI/180.0f, gy*PI/180.0f, gz*PI/180.0f,  my,  mx, mz);
    /*MahonyQuaternionUpdate(myIMU.ax, myIMU.ay, myIMU.az, myIMU.gx*DEG_TO_RAD,
                         myIMU.gy*DEG_TO_RAD, myIMU.gz*DEG_TO_RAD, myIMU.my,
                         myIMU.mx, myIMU.mz, myIMU.deltat);*/
                         
  
    MadgwickQuaternionUpdate(myIMU.ax, myIMU.ay, myIMU.az, myIMU.gx*DEG_TO_RAD,
                         myIMU.gy*DEG_TO_RAD, myIMU.gz*DEG_TO_RAD, myIMU.my,
                         myIMU.mx, myIMU.mz, myIMU.deltat);

    // Serial print and/or display at 0.5 s rate independent of data rates
    myIMU.delt_t = millis() - myIMU.count;

    // Print delay in milliseconds
    if (myIMU.delt_t > 50){
// Define output variables from updated quaternion---these are Tait-Bryan
// angles, commonly used in aircraft orientation. In this coordinate system,
// the positive z-axis is down toward Earth. Yaw is the angle between Sensor
// x-axis and Earth magnetic North (or true North if corrected for local
// declination, looking down on the sensor positive yaw is counterclockwise.
// Pitch is angle between sensor x-axis and Earth ground plane, toward the
// Earth is positive, up toward the sky is negative. Roll is angle between
// sensor y-axis and Earth ground plane, y-axis up is positive roll. These
// arise from the definition of the homogeneous rotation matrix constructed
// from quaternions. Tait-Bryan angles as well as Euler angles are
// non-commutative; that is, the get the correct orientation the rotations
// must be applied in the correct order which for this configuration is yaw,
// pitch, and then roll.
// For more see
// http://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
// which has additional links.
      myIMU.yaw   = atan2(2.0f * (*(getQ()+1) * *(getQ()+2) + *getQ() * *(getQ()+3)),
                          *getQ() * *getQ() + *(getQ()+1) * *(getQ()+1) - *(getQ()+2) * *(getQ()+2) - *(getQ()+3) * *(getQ()+3));
                    
      myIMU.pitch = -asin(2.0f * (*(getQ()+1) * *(getQ()+3) - *getQ() *
                    *(getQ()+2)));
                    
      myIMU.roll  = atan2(2.0f * (*getQ() * *(getQ()+1) + *(getQ()+2) * *(getQ()+3)),
                          *getQ() * *getQ() - *(getQ()+1) * *(getQ()+1) - *(getQ()+2) * *(getQ()+2) + *(getQ()+3) * *(getQ()+3));
                    
      myIMU.pitch *= RAD_TO_DEG;
      myIMU.yaw   *= RAD_TO_DEG;
      // Declination of SparkFun Electronics (40°05'26.6"N 105°11'05.9"W) is
      //   8° 30' E  ± 0° 21' (or 8.5°) on 2016-07-19
      // - http://www.ngdc.noaa.gov/geomag-web/#declination
      //myIMU.yaw   -= 0.331613;
      myIMU.yaw   -= 1.9;
      myIMU.roll  *= RAD_TO_DEG;


// Este codigo es que agrega los valores al mensaje.
      *mns+="ejeX:";
      String pitch = String(myIMU.pitch);
      *mns+=pitch;
      
      *mns+=";ejeY:";       
      String roll = String(myIMU.roll);
      *mns+=roll;
      
      myIMU.count = millis();
      myIMU.sumCount = 0;
      myIMU.sum = 0;
    }
}
