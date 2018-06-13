// EmonLibrary examples openenergymonitor.org, Licence GNU GPL V3

#include "EmonLib.h"             // Include Emon Library
EnergyMonitor emon1;             // Create an instance

int i = 0;
float tenvals = 0.0;
float minval = 1000;
float maxval = 0.0;

void setup()
{  
  Serial.begin(115200);
  
  emon1.voltage(A0, 440, 1.7);  // Voltage: input pin, calibration, phase_shift
//  emon1.current(1, 111.1);       // Current: input pin, calibration.
}

void loop()
{
  emon1.calcVI(30,1000);         // Calculate all. No.of half wavelengths (crossings), time-out
  //emon1.serialprint();           // Print out all variables (realpower, apparent power, Vrms, Irms, power factor)
  
  /*float realPower       = emon1.realPower;        //extract Real Power into variable
  float apparentPower   = emon1.apparentPower;    //extract Apparent Power into variable
  float powerFActor     = emon1.powerFactor;      //extract Power Factor into Variable
  float supplyVoltage   = emon1.Vrms;             //extract Vrms into Variable
  float Irms            = emon1.Irms;             //extract Irms into Variable*/

 float Vrms = (emon1.Vrms);
 if (Vrms < 0) { Vrms = 0.0; }
 
 tenvals += Vrms;
 if (minval > Vrms) { minval = Vrms; }
 if (maxval < Vrms) { maxval = Vrms; }
 
 i++;

  char comando = '1';
  String retorno = "" + millis();
  if (Serial.available() > 0) {
    comando = Serial.read();
    if (comando == 's' ){
      Serial.print("Avg: ");
      Serial.print(tenvals/i);
      Serial.print(" (");
      Serial.print(Vrms);
      Serial.print(") Min: ");
      Serial.print(minval);
      Serial.print(" Max: ");
      Serial.println(maxval);
    } 
    if (comando == 'm' ){
      Serial.println(tenvals/i);
    }
    if (comando == 'l' ){
      minval = 1000.0;
      maxval = 0;
    }
    if (comando == 'a' ){
      Serial.print(minval);
      Serial.print(":");
      Serial.println(maxval);
    }
    if (comando == 'v' ){
      Serial.println(Vrms);
    }
    

  }


 if (i == 20)
 {
  i = 0;
  tenvals = 0.0;
  //minval = 1000.0;
  //maxval = 0.0;
 }
  delay(50);  
}
