#include <ESP8266WiFi.h>

// conexion a router
#define MAX_SRV_CLIENTS 1
// puerto del server
#define PORT 7070
const char* ssid = "WiFiCar";
const char* password = "pass1234";

// servidor con el puerto y variable con la maxima cantidad de 

WiFiServer server(PORT);
WiFiClient serverClients[MAX_SRV_CLIENTS];

unsigned long previousMillis = 0;
const long interval = 200;

#define EnA D5 // 
#define In1 D4 // 
#define In2 D3 // 0
#define In3 D2 // 1 para ir hacia adelante
#define EnB D1 // 
#define In4 D0 // 0 para ir hacia adelante


//
bool Turn [2] = {};
bool CarMove [2] = {};
int vel = 0;
bool dir = 0;
byte luces = B11111111;

void setup() {
  Serial.begin(115200);
  pinMode(In1,OUTPUT);
  pinMode(In2,OUTPUT);
  pinMode(In3,OUTPUT);
  pinMode(In4,OUTPUT);
  pinMode(EnA,OUTPUT);
  pinMode(EnB,OUTPUT);
  Serial.begin(115200);

  IPAddress ip(192,168,43,200);
  IPAddress gateway(192,168,43,1);
  IPAddress subnet(255,255,255,0);

  WiFi.config(ip, gateway, subnet);

  WiFi.mode(WIFI_STA);

  WiFi.begin(ssid, password);
  
  uint8_t i = 0;
  while (WiFi.status() != WL_CONNECTED && i++ < 20) delay(500);
  if (i == 21) {
    Serial.print("Could not connect to: "); Serial.println(ssid);
    while (1) delay(500);
  } else {
    Serial.println("It´s connected");
  }
  server.begin();
  server.setNoDelay(true);

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
        // lo que hace el cliente
        if(process(serverClients[i].readStringUntil('\r'))){
          serverClients[i].println("ok;");  
        }
        else{
          serverClients[i].println("bad");
        }
        serverClients[i].stop();
      }
    }
  }
  digitalWrite(In1,Turn[0]);
  digitalWrite(In2,Turn[1]);  
  digitalWrite(In3,CarMove[0]);
  digitalWrite(In4,CarMove[1]);
  digitalWrite(EnB, dir);
  analogWrite(EnA, vel);
  delay(5);
}

bool process(String input){
  int begin = 0, delComa, del2puntos;
  bool result = false;
  delComa = input.indexOf(';',begin);
  
  while(delComa>0){
  
    String command = input.substring(begin, delComa);
  
    del2puntos = command.indexOf(':');
    
    if(del2puntos>0){
      String llave = command.substring(0,del2puntos);
      String valor = command.substring(del2puntos+1);
      definir(llave,valor, &result);
    }
    delComa = input.indexOf(';',begin);
  }
  return result;
}

void definir(String llave, String valor, bool *result){
  Serial.println(valor.toInt());
  Serial.println(valor.toInt());
  *result = true;
  if(llave == "pwm"){
    vel = valor.toInt();
    if(vel<0){
      vel *= -1;
      reverse();
    } 
    else{
      forward();
    }
  }
  
  else if(llave == "dir"){
    switch (valor.toInt()){
      case 1:
        Serial.println("Girando derecha");
        turnright();
        break;
      case -1:
        Serial.println("Girando izquierda");
        turnleft();
        break;
       default:
        Serial.println("directo");
        straight();
        break;
    }
  }
  else if(llave == "ld"){
    if(valor.toInt()>0 and luces%10<1){
      luces+=B1;
    }
    else{
      luces-=B1;
    }
  }
  else if(llave == "lt"){
    if(valor.toInt()>0){
      if(luces%100<10){
        luces+=B10;
      }
    }
    else{
      luces-=B10;
    }
  }
  else if(llave == "izq"){
    if(valor.toInt()>0){
      if(luces%1000<B100){
        luces+=B0000100;
      }
    }
    else{
      luces-=B00000100;
    }
  }
  else if(llave == "der"){
    if(valor.toInt()>0){
      if(luces%10000<B1000){
        luces+=B1000;
      }
    }
    else{
      luces-=B1000;
    }
  }
  
  else{
    Serial.println("Recived undefined Key value");
    *result = false;
  }
}


void straight(){
  dir = 0;
}

void turnright(){
  dir = 1;
  Turn[0] = 1;
  Turn[1] = 0;
}

void turnleft(){
  dir = 1;
  Turn[0] = 0;
  Turn[1] = 1;
}

void forward(){
  CarMove[0] = 0;
  CarMove[1] = 1;
}

void reverse(){
  CarMove[0] = 1;
  CarMove[1] = 0;
}

void stopCar(){
  vel = 0;
  dir = 0;
}
