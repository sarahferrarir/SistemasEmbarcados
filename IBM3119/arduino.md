// Calibrating the load cell
#include "HX711.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 6;
const int LOADCELL_SCK_PIN = 7;

HX711 scale;

void setup() {
  Serial.begin(57600);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
    if (scale.is_ready()) {
    scale.set_scale();    
    scale.tare();}
}

void loop() {
  delay(1000);

  if (scale.is_ready()) {
    long reading = scale.get_units(10);
    Serial.println((reading -11) / 224.1);
  } 
  else {
    Serial.println("HX711 not found.");
  }
}

//calibration factor will be the (reading)/(known weight)
// Peso * 10 = ((Leitura_ADC - 11) * 100) / 2241
