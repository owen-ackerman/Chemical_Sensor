
#include "Adafruit_CCS811.h"

Adafruit_CCS811 ccs;

int TVOC;
int RedLED = 2;
int GreenLED = 5;
int BlueLED = 4;
int  buzzer = 3;
int VOCLow = 40;
int VOCMed = 100;
int BuzzHz = 741;

void setup() {
  Serial.begin(115200);
  if(!ccs.begin()){
    Serial.println("Failed to start sensor! Please check your wiring.");
  }

   pinMode(RedLED, OUTPUT);
   pinMode(GreenLED, OUTPUT);
   pinMode(BlueLED, OUTPUT);
  // Wait for the sensor to be ready
}

void RGB_LED(int Red, int Green, int Blue) {
  analogWrite(RedLED, Red);
  analogWrite(GreenLED, Green);
  analogWrite(BlueLED, Blue);
}

void loop(){
if(ccs.available()){
    int eCO2 = ccs.geteCO2(); //returns eCO2 reading
    int TVOC = ccs.getTVOC(); //return TVOC reading
    float temp = ccs.calculateTemperature();
  if(ccs.readData()){
      Serial.print("CO2: ");
      Serial.print(eCO2);
      Serial.print("ppm, TVOC: ");
      Serial.println(TVOC);
    }
  
  RGB_LED(0, 0, 0);
  noTone(buzzer);
  if (TVOC < VOCLow){
      RGB_LED(0, 255, 0); 
      
    }

  if (TVOC > VOCLow && TVOC < VOCMed){
      RGB_LED(0, 255, 255);
              
    }

  if (TVOC > VOCMed){
      RGB_LED(255, 0, 0);
      tone(buzzer, BuzzHz);
    }
  }
}