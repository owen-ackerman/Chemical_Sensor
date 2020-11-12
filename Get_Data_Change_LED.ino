

void loop() {
  
  if(ccs.available()){
    int eCO2 = ccs.geteCO2(); //returns eCO2 reading
    int TVOC = ccs.getTVOC(); //return TVOC reading
    float temp = ccs.calculateTemperature();
  if(ccs.readData()){
      Serial.print("CO2: ");
      Serial.print(ccs.geteCO2());
      Serial.print("ppm, TVOC: ");
      Serial.println(ccs.getTVOC());
    }
    
    digitalWrite(LEDState, LOW);
    noTone(buzzer);
    
    if (TVOC < VOCLow){
      LEDState = 13; 
      
    }
    if (TVOC > VOCLow && TVOC < VOCMed){
      LEDState = 12;  
              
    }
     if (TVOC > VOCMed){
      LEDState = 11;
      tone(buzzer, BuzzHz);
      
    }
     digitalWrite(LEDState, HIGH); 
     
  }
 // delay(250);
}
