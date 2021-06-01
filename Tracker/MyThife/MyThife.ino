//---------------------Inclusions------------------------//
#include <SoftwareSerial.h>
#include "Adafruit_FONA.h"
#include "config.h"

//---------------------Globals------------------------//
#define FONA_TX 13        //RX on Sim808
#define FONA_RX 15        //TX on Sim808
#define FONA_RST 5        //Reset Pin
#define FONA_RI 2         //Ring Pin for incoming Messages
#define LED LED_BUILTIN   //For Debuging
#define BUSYWAIT 15000    //Pause Time

char pin[] = PIN;

char replybuffer[255];
char callerIDbuffer[32];
char sender[25];
uint8_t n = 1;


float latitude, longitude, speed_kph, heading, speed_mph, altitude;
float dateTime;
char gpsdata[120];    //Array for holding the AT response
char imei[15] = {0};  // MUST use a 16 character buffer for IMEI!

//---------------------Setup------------------------//
SoftwareSerial fonaSS = SoftwareSerial(FONA_TX, FONA_RX);
Adafruit_FONA fona = Adafruit_FONA(FONA_RST);
uint8_t readline(char *buff, uint8_t maxbuff, uint16_t timeout = 0);

//Init function
boolean fonaInit(void){
  Serial.println(F("Initializing....(May take 3 seconds)"));
  digitalWrite(LED, HIGH);
  delay(100);
  digitalWrite(LED, LOW);
  delay(100);
  digitalWrite(LED, HIGH);
  delay(100);
  digitalWrite(LED, LOW);
  delay(100);


  // Starting The communication, make it slow so its easy to read!
  fonaSS.begin(9600);       // if you're using software serial
  //Serial1.begin(4800);    // if you're using hardware serial

  // See if the FONA is responding
  if (! fona.begin(fonaSS)) {               // can also try fona.begin(Serial1) 
    Serial.println(F("Couldn't find FONA"));
    return false;
  }
  Serial.println(F("FONA is OK"));
  return true;
}


void setup() {
  //Start up Com and set up LED
  pinMode(LED, OUTPUT);
  pinMode(FONA_RI, INPUT);
  digitalWrite(FONA_RI, HIGH); // turn on pullup on RI

  Serial.begin(9600);
  Serial.println(F("FONA basic test"));

  //Wait till Fona is online
  while (! fonaInit()) {
    delay(5000);
  }
  //Unlock Sim and Read the Devices IMEI
  fona.unlockSIM(pin);
  uint8_t imeiLen = fona.getIMEI(imei);  //get the Length and store the IMEI in its array

  if (imeiLen > 0) {
    Serial.print("SIM card IMEI: "); Serial.println(imei);
  }

  fona.enableGPS(true);
  fona.sendCheckReply(F("AT+CFGRI=1"), F("OK"));
  fona.setGPRSNetworkSettings(F(APN), F(USER), F(PASSWORD));
  fona.enableNetworkTimeSync(true);

  //turn on GPRS And wait for it to report
  while(!fona.enableGPRS(true)){
    Serial.println(F("Failed to turn on"));
    delay(1000);
  } 

  // print Report and turn on LED 3 times
  Serial.println(F("GPRS ON"));
  blinkLED(3,200);

  //Clear SMS Cache
  if(delSMS()){
    Serial.println("All SMS Deleted");
  }

  //Atach the interrupt for a call to wake up
  //attachInterrupt(digitalPinToInterrupt(FONA_RI), start, CHANGE);
}


void loop() {
  upload();
  uint16_t vbat;
  if (! fona.getBattVoltage(&vbat)) {
    Serial.println(F("Failed to read Batt"));
  } else {
    Serial.print(F("VBat = ")); Serial.print(vbat); Serial.println(F(" mV"));
  }

  delay(20000);

}

//---------------------Helper Functions------------------------//
void blinkLED(int number, int Time){

  for(int i=0; i<number; i++){
    
    digitalWrite(LED, HIGH);
    delay(Time);
    digitalWrite(LED, LOW);
    delay(Time);
  }
}


boolean delSMS(){
  int8_t smsnum = fona.getNumSMS();
  if (smsnum < 0) {
    Serial.println(F("Could not read # SMS"));
    return false;
  } else {
    Serial.print(smsnum); 
    Serial.println(F(" SMS's on SIM card!"));
  }
  
  if (smsnum == 0) return false;

  // there's an SMS!
  n = 1; 
  while (smsnum>=n) {
     uint16_t smslen;
     char sender[25];
     int16_t length;

     
     Serial.print(F("\n\rReading SMS #")); Serial.println(n);
     uint8_t len = fona.readSMS(n, replybuffer, 250, &smslen); // pass in buffer and max len!
     // if the length is zero, its a special case where the index number is higher
     // so increase the max we'll look at!
     if (len == 0) {
        Serial.println(F("[empty slot]"));
        n++;
        continue;
     }
     if (! fona.getSMSSender(n, sender, sizeof(sender))) {
       // failed to get the sender?
       sender[0] = 0;
     }
     
     Serial.print(F("***** SMS #")); Serial.print(n);
     Serial.print(" ("); Serial.print(len); Serial.println(F(") bytes *****"));
     Serial.println(replybuffer);
     Serial.print(F("From: ")); Serial.println(sender);
     Serial.println(F("*****"));
     fona.deleteSMS(n);
     n++;
  }
  return true;
}

void upload(){
  if(fona.getGPS(&dateTime,&latitude, &longitude, &speed_kph, &heading, &altitude)){
      uint16_t statuscode;
      int16_t length;
      Serial.println(dateTime);
      double la= (double) latitude;
      double lo= (double) longitude;
      double sp= (double) speed_kph;
      double co= (double) heading;
      double ti= (double) dateTime;
      Serial.println(ti);
      char a[12];
      char b[12];
      char c[12];
      char d[12];
      char t[23];
      fona.getTime(t,23);
      t[0]='y';
      t[3]='m';
      t[6]='d';
      t[9]='h';
      t[12]='m';
      t[15]='s';
      t[18]='ms';
      t[21]='e';
      dtostrf(la, 1, 6,a);
      dtostrf(lo, 1, 7,b);
      dtostrf(sp, 1, 2,c);
      dtostrf(co, 1, 2,d);
      char data[255];
      sprintf(data, "http://intern.bewegtbildhelden.de/input?latitude=%s&longitude=%s&speed=%s&id=%s&time=%s", a,b,c,imei,t);
      Serial.println(data);
      if (!fona.HTTP_GET_start(data,&statuscode, (uint16_t *)&length)) {
          Serial.println("Failed!");
          fona.HTTP_GET_end();
      } else {
        Serial.println(F("Sent!"));
        /*while (length > 0) {
          while (fona.available()) {
            char c = fona.read();

#if defined(__AVR_ATmega328P__) || defined(__AVR_ATmega168__)
            loop_until_bit_is_set(UCSR0A, UDRE0);
            UDR0 = c;
#else
            Serial.write(c);
#endif

            length--;
            if (! length) break;
          }
        }*/
        fona.HTTP_GET_end();
      }
      }
}
