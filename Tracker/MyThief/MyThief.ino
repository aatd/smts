//-------------------Includes-------------------//

#include <Arduino.h>
#include "config.h"
#include "Adafruit_FONA.h"
#include <math.h>

// For ESP32 hardware serial
#include <HardwareSerial.h>

//-------------------Defines-------------------//
// Define *one* of the following lines:
//#define SIMCOM_2G // SIM800/808/900/908, etc.
//#define SIMCOM_3G // SIM5320
#define SIMCOM_7000
//#define SIMCOM_7070
//#define SIMCOM_7500
//#define SIMCOM_7600

// For botletics SIM7000 shield with ESP32
#define FONA_PWRKEY 4
#define FONA_RST 5
#define FONA_TX 26 // ESP32 hardware serial RX2 (GPIO16)
#define FONA_RX 27 // ESP32 hardware serial TX2 (GPIO17)

// For botletics SIM7500 shield
//#define FONA_PWRKEY 6
//#define FONA_RST 7
//#define FONA_DTR 9 // Connect with solder jumper
//#define FONA_RI 8 // Need to enable via AT commands
//#define FONA_TX 11 // Microcontroller RX
//#define FONA_RX 10 // Microcontroller TX
//#define T_ALERT 5 // Connect with solder jumper

#define LED 12  //For Debuging


HardwareSerial fonaSS(1);

// Use this for 2G modules
#ifdef SIMCOM_2G
Adafruit_FONA fona = Adafruit_FONA(FONA_RST);

// Use this one for 3G modules
#elif defined(SIMCOM_3G)
Adafruit_FONA_3G fona = Adafruit_FONA_3G(FONA_RST);

// Use this one for LTE CAT-M/NB-IoT modules (like SIM7000)
// Notice how we don't include the reset pin because it's reserved for emergencies on the LTE module!
#elif defined(SIMCOM_7000) || defined(SIMCOM_7070) || defined(SIMCOM_7500) || defined(SIMCOM_7600)
Adafruit_FONA_LTE fona = Adafruit_FONA_LTE();
#endif

//-------------------Globals-------------------//

uint8_t readline(char *buff, uint8_t maxbuff, uint16_t timeout = 0);
uint8_t type;
char pin[] = PIN;
char replybuffer[255]; // this is a large buffer for replies
char imei[16] = {0}; // MUST use a 16 character buffer for IMEI!



float latitude, longitude, speed_kph, heading, altitude, sec; //used for storing GPS parameters
uint16_t vbat, year;
uint8_t month,day,hour,minute;

uint16_t lowWarn=10;

int GPRSFailCount,GPSFailCount=0;

unsigned long batLastChecked=millis();
unsigned long moveLastChecked=millis();
unsigned long movementInterval=60000;
unsigned long stopInterval=600000;
unsigned long trackingInterval=stopInterval;
int movementCount=0;
int stopCount=0;

bool batWarningSent = false;
//-------------------Init-------------------//
void setup() {

    //Setting Reset
    pinMode(FONA_RST, OUTPUT);
    digitalWrite(FONA_RST, HIGH); // Default state
    pinMode(LED, OUTPUT);
    digitalWrite(LED, HIGH); // Default state

    // Turn on the module by pulsing PWRKEY low for a little bit
    // This amount of time depends on the specific module that's used
    fona.powerOn(FONA_PWRKEY); // Power on the module
    delay(5000);
    Serial.begin(9600);  //Set the boudrate
    Serial.println(F("ESP32 SIMCom Basic Test"));
    Serial.println(F("Initializing....(May take several seconds)"));

    Serial.println(F("Configuring to 9600 baud"));
    fonaSS.println("AT+IPR=9600"); // Set baud rate
    delay(100); // Short pause to let the command run
    fonaSS.begin(9600, SERIAL_8N1, FONA_TX, FONA_RX); // Switch to 9600
/*

*/
    //Connect with AT Command
    while(!fona.begin(fonaSS)){
        if (! fona.begin(fonaSS)) {
            Serial.println(F("Couldn't find FONA"));
            fona.powerOn(FONA_PWRKEY); // Power on the module
            delay(5000); //Wait 5 Sekonds

        }
    }
    uint8_t imeiLen = fona.getIMEI(imei);
    if (imeiLen > 0) {
        Serial.print("Module IMEI: "); Serial.println(imei);
    }
    //Setup Network settings
    fona.setNetworkSettings(F(APN), F(USER), F(PASSWORD));
    delay(1000);
    initPin();
    delay(1000);
    //Enable GPRS
    initGPRS();
    delay(1000);

    //enable the GPS module
    initGPS();
    checkBattery();
    checkMovement();

    

}

void loop() {
    if((millis()-batLastChecked)>600000){
        checkBattery();
    }
    if((millis()-moveLastChecked)>trackingInterval){
        checkMovement();
        status();
    }

}


//-------------------Helper-------------------//

void initPin(){ //initialises the PIN, if not possible restarts the Device
    while(fona.unlockSIM(pin)!=1){
        Serial.println("Pin not accepted... Retry in 10 Seconds");
        fona.powerOn(FONA_PWRKEY); // Power on the module
        delay(10000);
        fona.begin(fonaSS);
        fona.setNetworkSettings(F(APN), F(USER), F(PASSWORD));
        delay(1000);
    }
    Serial.println("Pin Accepted");
}

void initGPRS(){ //Iitialises Network connection
    while(!fona.enableGPRS(true)&&(GPRSFailCount<10)) {
        Serial.println("GPRS Faild, Retray in...");
        Serial.println("3...");
        delay(1000);
        Serial.println("2...");
        delay(1000);
        Serial.println("1...");
        delay(1000);
        GPRSFailCount++;
    }

    if(GPRSFailCount>=10){
        GPRSFailCount=0;
        initPin();
    }
    Serial.println("gprs enabled");
}

void initGPS(){
    while(!fona.enableGPS(true)&&(GPSFailCount<10)){
        initGPRS();
        GPSFailCount++;
    }
    Serial.println("GPS Enabled");
}

void checkBattery(){

    if (! fona.getBattPercent(&vbat)) {
        Serial.println(F("Failed to read Batt"));
    } else {
        Serial.print(F("VPct = ")); Serial.print(vbat); Serial.println(F("%"));
        batLastChecked=millis();
    }

    if(vbat<lowWarn&&!batWarningSent) sendBatWarning();
    if(batWarningSent&&vbat>lowWarn+5) batWarningSent=false;

}

void sendBatWarning(){
    if (!fona.sendSMS(OWNER, "Battery Status lower 10%")) {
        Serial.println(F("Failed"));
    } else {
        Serial.println(F("Sent!"));
        batWarningSent=true;
    }
}

void checkMovement(){
    double lat=latitude;
    double lon = longitude;

    for(int i=0; i<=10; i++){
        if(fona.getGPS(&latitude, &longitude, &speed_kph, &heading, &altitude,&year, &month, &day, &hour, &minute,&sec)) break;
        gpsFail();
        delay(5000);
    }

    double R = 6371000; // metres
    double latRad = latitude * M_PI/180; // Coordinates in radians
    double latRadOld = lat * M_PI/180;
    double deltaLatRad = (latRadOld-latRad) * M_PI/180;
    double deltaLonRad = (lon-longitude) * M_PI/180;

    double a = sin(deltaLatRad/2) * sin(deltaLatRad/2) +
              cos(latRad) * cos(latRadOld) *
              sin(deltaLonRad/2) * sin(deltaLonRad/2);
    double c = 2 * atan2(sqrt(a), sqrt(1-a));

    double d = R * c; // in metres

    Serial.println ("distance is ");
    Serial.print (d);
    Serial.print(" metres");

    if(d>10){
        movementCount++;
        stopCount=0;
        trackingInterval = movementInterval;
    }
    if(movementCount>3) { uploadPosition(); }

    if(d<2){ movementCount=0; stopCount++;}
    if(stopCount>10)trackingInterval=stopInterval;
    moveLastChecked=millis();

}

void uploadFaildSignal(){
    digitalWrite(LED, HIGH);
    delay(1000);
    digitalWrite(LED, LOW);
    delay(1000);
    digitalWrite(LED, HIGH);
    delay(1000);
    digitalWrite(LED, LOW);
}

void uploadSuccessSignal(){
    digitalWrite(LED, HIGH);
    delay(200);
    digitalWrite(LED, LOW);
    delay(200);
    digitalWrite(LED, HIGH);
    delay(200);
    digitalWrite(LED, LOW);
    delay(200);
    digitalWrite(LED, HIGH);
    delay(200);
    digitalWrite(LED, LOW);
    delay(200);
    digitalWrite(LED, HIGH);
    delay(200);
    digitalWrite(LED, LOW);
    delay(200);
}

void status(){
    digitalWrite(LED, HIGH);
    delay(200);
    digitalWrite(LED, LOW);
    delay(200);
    digitalWrite(LED, HIGH);
    delay(200);
    digitalWrite(LED, LOW);
}

void gpsFail(){
    digitalWrite(LED, HIGH);
    delay(100);
    digitalWrite(LED, LOW);
    delay(100);
    digitalWrite(LED, HIGH);
    delay(100);
    digitalWrite(LED, LOW);
    delay(100);
    digitalWrite(LED, HIGH);
    delay(100);
    digitalWrite(LED, LOW);
    delay(100);
    digitalWrite(LED, HIGH);
    delay(100);
    digitalWrite(LED, LOW);
    delay(100);
    digitalWrite(LED, HIGH);
    delay(100);
    digitalWrite(LED, LOW);
    delay(100);
    digitalWrite(LED, HIGH);
    delay(100);
    digitalWrite(LED, LOW);
}

void uploadPosition(){
    char data[255];
    char cJson[255];
    uint16_t statuscode;
    int16_t length;

    char lat[12];
    char lon[12];

    dtostrf(double(latitude), 1, 6,lat);
    dtostrf(double(longitude), 1, 7,lon);


    sprintf(data, "%s/devices/%s/locations",UPLOADURL,imei);
    Serial.println(data);
    sprintf(cJson, "{\"latitude\":%s,\"longitude\":%s,\"velocity\":%s,\"battery\":%s,\"time\":\"%d-%d-%d %d:%d:%s\"}",lat,lon,String(speed_kph),String(vbat),year,month,day,hour,minute,String(sec));
    Serial.println(cJson);
    if (!fona.HTTP_POST_start(data,F("application/json"),(uint8_t *) cJson, strlen(cJson), &statuscode, (uint16_t *)&length)) {
        Serial.println("Failed!");
        uploadFaildSignal();
        fona.HTTP_POST_end();
    } else {
        Serial.println(F("Sent!"));
        uploadSuccessSignal();

        while (length > 0) {
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
        }
        fona.HTTP_POST_end();
    }
}