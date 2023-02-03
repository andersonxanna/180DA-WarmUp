/*
From https://learn.sparkfun.com/tutorials/esp32-s2-thing-plus-hookup-guide/all 
*/
int ledPin = 2; //Pin on my esp32 for onboard LED

void setup()
{
    pinMode(ledPin, OUTPUT);
    Serial.begin(115200);
}

void loop()
{
    Serial.println("Hello, world!");
    digitalWrite(ledPin, HIGH);
    delay(500);
    digitalWrite(ledPin, LOW);
    delay(500);
}
