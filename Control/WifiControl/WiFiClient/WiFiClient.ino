// Hardware setup:
// MPU9250 Breakout --------- Arduino
// VDD ---------------------- 3.3V
// VDDI --------------------- 3.3V
// SDA ----------------------- A4
// SCL ----------------------- A5
// GND ---------------------- GND

#include "quaternionFilters.h"
#include "MPU9250.h"
#include <Wire.h>
#include <ESP8266WiFi.h>

//Constants for network connection 
const char* ssid      = "WiFiCar2";
const char* password  = "pass1234";
const char* host      = "192.168.43.252";
const int   port      = 8010;

//Device instances being used
MPU9250     myIMU;
WiFiClient  client;

//Task constants and variables
const uint8_t           maxAttempsNetwork = 20;
const uint8_t           maxAttempsHost    = 20;
const unsigned long int interval          = 50;

float pitch;
float roll;
float yaw;



void setup() {
  Wire.begin(0, 2);
  Serial.begin(115200);
  delay(10);

  connectESP();
  connectMPU();
  
}

void connectESP(){
  //Connecting to the wifi network
  Serial.println("\n\nConnecting to" + String(ssid));
  //Sets ESP8266 to be a client explicitly
  WiFi.mode(WIFI_STA); 
  //Connects to the network
  WiFi.begin(ssid, password);

  //Tries to connect to a network as a client as many times
  for(uint8_t attempt = 0; attempt < maxAttempsNetwork; ++attempt){
    if(WiFi.status() == WL_CONNECTED) break;
    delay(500); //Try check 500ms later
    Serial.printf("Attempt %d failed to connect to network\n", attempt);
  }

  //Check for connection one more time and tries to connect to server
  if(WiFi.status() == WL_CONNECTED){
    Serial.println("WiFi connected to IP: " + client.localIP());
    Serial.println("Trying to connect to host: " + String(host));
    
    //Attempts to connect to host
    uint8_t hostAttempt = 0;
    for(; hostAttempt < maxAttempsHost; ++hostAttempt){
      if(client.connect(host, port)){
        hostAttempt = 0; //Condition to check later
        break;
      }
      Serial.printf("Attempt %d failed to connect to host\n", hostAttempt);
      delay(2000);
    } 
    
    //It connected 
    if(hostAttempt == 0) Serial.println("Fully connected");
    else Serial.println("Failed to connect to host");
  }
  else Serial.println("WiFi could not connect");
}

void connectMPU(){
  byte c = myIMU.readByte(MPU9250_ADDRESS, WHO_AM_I_MPU9250);
  //Checks for connection of MPU
  if(c == 0x71){
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
    Serial.printf("Could not connect to MPU9250: 0x%x", c);
  }
}

void readMPU(float& _pitch, float& _roll, float& _yaw){
  if (myIMU.readByte(MPU9250_ADDRESS, INT_STATUS) & 0x01){  
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

      //Saves values in the variables passed
      _pitch = myIMU.pitch;
      _roll  = myIMU.roll;
      _yaw   = myIMU.yaw;
      
      myIMU.count = millis();
      myIMU.sumCount = 0;
      myIMU.sum = 0;
    }
}

//Sends message using ESP connection to host
void sendMessage(String _message){
  if(client.connected()) client.print(_message + "\r");
  else Serial.println("Couldn't send message:\n " + _message + + "\nTo host\n");
}

//Checks if ESP is still connected
void checkESP(){
  if(!client.connected()){
    while (!client.connect(host, port)){
      Serial.println("Knocked down");
    }
  }
}

void loop() {
  Serial.println("Reading and sending once");
  readMPU(pitch, roll, yaw);
  String message = "";
  message += "ejeX:" + String(pitch) + ";";
  message += "ejeY:" + String(roll) + ";";
  message += "ejeZ:" + String(yaw) + ";";
  sendMessage(message);
  Serial.println(message);
  checkESP();
  delay(interval);

  // Read all the lines of the reply from server and print them to Serial
  /*while (client.available()) {
    String line = client.readStringUntil('\r');
    Serial.print(line);
  }*/
}
