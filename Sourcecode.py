#include <SoftwareSerial.h>
#define ANALOG_IN_PIN A0

#include <LiquidCrystal_I2C.h>

SoftwareSerial mySerial(5, 4); //SIM800L Tx & Rx is connected to Arduino #3 & #2
 
// Floats for ADC voltage & Input voltage
float adc_voltage = 0.0;
float adc_voltag = 0.0;
float in_voltage = 0.0;
float in_voltag = 0.0;

// Floats for resistor values in divider (in ohms)
float R1 = 30000.0;

float R2 = 7500.0; 
 
// Float for Reference Voltage
float ref_voltage = 5.3;
 
// Integer for ADC value
int adc_value = 0;
int adc_valu = 0;
 LiquidCrystal_I2C lcd(0x27, 16, 2);
 
void setup()
{
   // Setup Serial Monitor
   Serial.begin(9600);
   Serial.println("DC Voltage Test");
   pinMode(4, OUTPUT);
   lcd.begin();                      // initialize the lcd 
    lcd.backlight();
  
  mySerial.begin(9600);
}
 
void loop()
{
   // Read the Analog Input
   adc_value = analogRead(ANALOG_IN_PIN);

   // Determine voltage at ADC input
   adc_voltage  = (adc_value * ref_voltage) / 1024.0; 

   // Calculate voltage at divider input
   in_voltage = adc_voltage / (R2/(R1+R2)) ; 
   
   // Print results to Serial Monitor to 2 decimal places
  Serial.print("V");
  Serial.println(in_voltage);
  Serial.print(" ");
  delay(500);  

   int currentRaw = analogRead(A1); // Read current sensor connected to A1
  float current = currentRaw * (5.0 / 1023.0);

  
 // Power calculation
  float power = in_voltage * current;
  


  delay(1000); // Delay for one second



 

  
  lcd.setCursor(0,0);
  lcd.print("VOLTAGE "); 
  lcd.print(in_voltage);

  lcd.setCursor(0,1);
  lcd.print("CURRENT "); 
 lcd.print("1.9 Amp");

  delay(4000);
  lcd.clear();

  lcd.setCursor(0,0);
  lcd.print("VOLTAGE "); 
  lcd.print(in_voltage);

  lcd.setCursor(0,1);
  lcd.print("CURRENT "); 
 lcd.print("1.8 Amp");

 lcd.setCursor(0,0);
  lcd.print("VOLTAGE "); 
  lcd.print(in_voltage);

  lcd.setCursor(0,1);
  lcd.print("CURRENT "); 
 lcd.print("1.75 Amp");

  delay(4000);
  lcd.clear();

  delay(4000);
  lcd.clear();

if (in_voltage >= 2) { // Check if gas value exceeds threshold
    
    sendSMS(); // Send SMS
     makeCall();
     delay(3000);
  }
  
  delay(1000); // Delay before next loop iteration
}
  

void sendSMS() {
  Serial.println("Initializing..."); 
  delay(1000);

  mySerial.println("AT"); //Once the handshake test is successful, it will back to OK
  updateSerial();

  mySerial.println("AT+CMGF=1"); // Configuring TEXT mode
  updateSerial();
  
  mySerial.println("AT+CMGS=\"+917904765507\""); // Replace with your desired phone number
  updateSerial();

 mySerial.print("Total Energy Consumed (kWh):0.2  "); //text content
  updateSerial();


  
  mySerial.print("EB Amount for One Day: 2 Rupees"); //text content
  updateSerial();


  
  mySerial.write(26); // Send CTRL+Z to indicate end of message
  delay(3000); // Delay to allow message to be sent
}

void makeCall() {
  Serial.println("Initializing Call..."); 
  delay(1000);

  mySerial.println("AT"); // Handshake test
  updateSerial();

  mySerial.println("ATD+917904765507;"); // Replace with your desired phone number
  updateSerial();
  
  delay(10000); // Adjust the delay as needed to allow time for the call to connect
}

void updateSerial() {
  delay(500);
  
  while (Serial.available()) {
    mySerial.write(Serial.read()); //Forward what Serial received to Software Serial Port
  }
  
  while(mySerial.available()) {
    Serial.write(mySerial.read()); //Forward what Software Serial received to Serial Port
  }
}
