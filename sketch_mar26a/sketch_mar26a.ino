int analogPin = A0; // potentiometer wiper (middle terminal) connected to analog pin 3
                    // outside leads to ground and +5V
int val = 0;  // variable to store the value read
int volt = 0;
int usl = 0;
byte maskb = B111111;
byte maskd = B11111100;
byte curr_maskb = maskb;
byte curr_maskd = maskd;
byte zeros[6] = {B011111, B101111, B110111, B111011, B111101, B111110};
int zerosd[6] = {B01111000, B10111000, B11011000, B11101000, B11110000, B11111000};
byte bdata[11];
int key = 2;


void setup() {
  Serial.begin(19200);   
  for (int i=2; i < 14; i++){
      pinMode(i, OUTPUT);
      digitalWrite (i, LOW);
    }
  pinMode(3, OUTPUT);   // D3 как выход
  delay(5);
}

int res = 0;
 
void loop() {
  if(key == 2){
  val = analogRead(analogPin);  // read the input pin
  Serial.println(val, DEC);
    if (Serial.available() > 0){
      key = Serial.read();
      return;
    }    
  delayMicroseconds (1);
  }
  
  if (key != 2) {
    if (key == 0){
      if (Serial.available() > 0){   
        res = Serial.readBytes(bdata, 11);
        usl = 1;
      }
      if (usl == 1){
        curr_maskb = maskb;
        curr_maskd = maskd;
        for (int i=0; i < 12; ++i){
          if(i < 6){
            if ((bdata[i] == byte(0))) {
            curr_maskb = curr_maskb & zeros[i];
            }
          }     
          if ((i >= 6) && (i!=11)) {
            if ((bdata[i] == byte(0))) {
            curr_maskd = curr_maskd & zerosd[i - 6];
           }
          }     
        }    
        PORTB = curr_maskb;
        PORTD = curr_maskd;
        if (bdata[0] == 0){
          digitalWrite (13, HIGH);
        }
        digitalWrite (2, HIGH);
        delay(200);
        digitalWrite (2, LOW);
        usl = 0;
      key = 2;
      }
    }
    
    if (key == 3){
      if (Serial.available() > 0){
        volt = Serial.read();
        usl = 1;
      }
      if (usl == 1){
        analogWrite(3, volt / 4);
        usl = 0;
        key = 2;
      }     
      
    }
  }
}
