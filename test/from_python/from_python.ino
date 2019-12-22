void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
}

void loop() {
  while( Serial.available() >0) {
    char c = Serial.read();
    if ( c =='y'){
      Serial.write('good');
      digitalWrite(13, HIGH);
    }
    else if( c =='n'){
      digitalWrite(13, LOW);
    }
  }
}
