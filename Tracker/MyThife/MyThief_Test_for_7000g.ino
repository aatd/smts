#include <ArduinoJson.h>

//Config
const char* APN      = ""; 
const char* PIN      = ""; 
const char* PASSWORD = ""; 
const char* USER     = ""; 
const char* BASEPATH = ""; 

//Debugging
bool debugLog = true;

//Inits the GSM Module
int initGSM()  {return 0;}

//Inits the GPRS Module
int initGPRS() {return 0;}

//Inits the GPS Module
int initGPS()  {return 0;}

//Update Configuration of the Module from a raw JSON File
int setConfig(const char* configJSON){

  Serial.println("My-Thief-setConfig() called.");
  Serial.print("-- Trying to set config with the input: ");
  Serial.println(configJSON);

  //Create JSON Doc
  StaticJsonDocument<300> doc;

  //Deserialize Doc
  DeserializationError error = deserializeJson(doc, configJSON);

  //Errorcheck
  if (error) {
    Serial.print(F("-- deserializeJson() failed: "));
    Serial.println(error.f_str());
    return 1;
  }
    
  APN      = doc["apn"];
  PIN      = doc["pin"];
  PASSWORD = doc["pwd"];
  USER     = doc["usr"];
  BASEPATH = doc["url"];
  Serial.print("-- APN is:      ");
  Serial.println(APN);
  Serial.print("-- PIN is:      ");
  Serial.println(PIN);
  Serial.print("-- PASSWORD is: ");
  Serial.println(PASSWORD);
  Serial.print("-- USER is:     ");
  Serial.println(USER);
  Serial.print("-- URL is:      ");
  Serial.println(BASEPATH);
  return 0;
}

//Checks the current Configuration
int checkConfig(){return 0;}

//Update internal Lifecycle
int updateLifecycle() {return 0;}

void setup() {
  Serial.begin(115200);
  while (!Serial);
  const char* json = "{\"apn\":\"internet.eplus.de\",\"pin\":\"1011\",\"pwd\":\"der_Ritter_Oder_so\",\"usr\":\"AATD\",\"url\":\"https://google.com.de.url\"}";
  int result = setConfig(json); 
}

void loop() {
//TODO
}
