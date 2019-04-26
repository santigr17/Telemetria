#include <ESP8266WiFi.h>

// conexion a router
#define MAX_SRV_CLIENTS 3
// puerto del server
#define PORT 7070

const char* ssid = "WiFiCar";
const char* password = "pass1234";


// servidor con el puerto y variable con la maxima cantidad de 

WiFiServer server(PORT);
WiFiClient serverClients[MAX_SRV_CLIENTS];

unsigned long previousMillis = 0, temp = 0;
const long interval = 100;

#define EnA D5 // 
#define In1 D4 // D4 en HIGH : retroceder
#define In2 D3 // D3 en HIGH : avanzar
#define In3 D2 // 
#define EnB D1 // 
#define In4 D0 // 0 para ir hacia adelante

/**
 * Lights
 * Babcdefgh
 * a: delanteras +
 * b: traseras
 * c: direccional izq
 * d: direccional der
 * e: 
 * f:
 * g:
 * h:
 */
#define clk D6
#define ab D7 


//
bool Turn [2] = {LOW,HIGH};
bool CarMove [2] = {HIGH,LOW};
int vel = 0;
bool dir = 0;
int battery = 0;
             //abcd 
byte luces = B00000000;

void setup() {
  Serial.begin(115200);
  pinMode(In1,OUTPUT);
  pinMode(In2,OUTPUT);
  pinMode(In3,OUTPUT);
  pinMode(In4,OUTPUT);
  pinMode(EnA,OUTPUT);
  pinMode(EnB,OUTPUT);
  pinMode(clk,OUTPUT);
  pinMode(ab,OUTPUT);
  
  IPAddress ip(192,168,43,200);
  IPAddress gateway(192,168,43,1);
  IPAddress subnet(255,255,255,0);

  WiFi.config(ip, gateway, subnet);

  WiFi.mode(WIFI_STA);

  WiFi.begin(ssid, password);
  
  uint8_t i = 0;
  while (WiFi.status() != WL_CONNECTED && i++ < 20) delay(500);
  if (i == 21) {
    Serial.print("\nCould not connect to: "); Serial.println(ssid);
    while (1) delay(500);
  } else {
    Serial.println("\nIt´s connected");
  }
  server.begin();
  server.setNoDelay(true);
  shiftOut(ab, clk, LSBFIRST, luces);

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
          String mensaje = serverClients[i].readStringUntil('\r');
          serverClients[i].flush();
          String respuesta; 
          process(mensaje, &respuesta);
          serverClients[i].println(respuesta);
          serverClients[i].stop();
        }  
      }
    }
  }
  digitalWrite(In3,Turn[0]);
  digitalWrite(In4,Turn[1]);  
  digitalWrite(In1,CarMove[0]);
  digitalWrite(In2,CarMove[1]);
  digitalWrite(EnB, dir);
  analogWrite(EnA, vel);
}

void process(String input, String * output){

  int comienzo = 0, delComa, del2puntos;
  bool result = false;
  delComa = input.indexOf(';',comienzo);
  
  while(delComa>0){
    String comando = input.substring(comienzo, delComa);

    del2puntos = comando.indexOf(':');
    
    if(del2puntos>0){
        String llave = comando.substring(0,del2puntos);
        String valor = comando.substring(del2puntos+1);
        *output += definir(llave,valor); 
      }
    else if(comando == "sense;"){
         *output += getSense();
    }     
    comienzo = delComa+1;
    delComa = input.indexOf(';',comienzo);
  }
}

String definir(String llave, String valor){
  String result="ok";;
  if(llave == "pwm"){
    vel = valor.toInt();
    if(vel<0){
      vel*=-1;
      reverse();
    }
    else{
      forward();
    }
  }
 
  else if(llave == "dir"){
    switch (valor.toInt()){
      case 1:
        turnright();
        break;
      case -1:
        turnleft();
        break;
       default:
        straight();
        break;
    }
  }
  else if(llave[0] == 'l'){
    bool encender = true;
    byte myBit = B00000000;
    if(valor == "0") encender = false;
    switch (llave[1]){
      case 'f':
        myBit = B01111111;      
        break;
      case 'b':
        myBit = B10111111;
        break;
      case 'l':
        myBit = B11011111;
        break;
      case 'r':
        myBit = B11101111;
        break;
      default:
        break;
    }
    if(encender) luces = luces & myBit;
    
    else{
      myBit = ~myBit;
      luces = luces|myBit;
    }
    shiftOut(ab, clk, MSBFIRST, luces);
  } 
  else{
    result = "Recived undefined key value: " + llave;
    Serial.println(result);
  }
  return result;
}

void straight(){
  dir = 0;
}

void turnright(){
  dir = HIGH;
  Turn[0] = HIGH;
  Turn[1] = LOW;
}

void turnleft(){
  dir = HIGH;
  Turn[0] = LOW;
  Turn[1] = HIGH;
}

void forward(){
  CarMove[0] = LOW;
  CarMove[1] = HIGH;
}

void reverse(){
  CarMove[0] = HIGH;
  CarMove[1] = LOW;
}

void stopCar(){
  vel = 0;
  dir = 0;
}

float getSense(){
  return analogRead(A0);
}

