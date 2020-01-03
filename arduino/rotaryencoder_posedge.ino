#define encoder0A 2
#define encoder0B 3

volatile unsigned int ctr = 0;

void setup() {
    //https://www.arduino.cc/en/Tutorial/InputPullupSerial
    pinMode(2, INPUT_PULLUP);
    pinMode(3, INPUT_PULLUP);
    //https://www.arduino.cc/reference/en/language/functions/external-interrupts/attachinterrupt/
    attachInterrupt(0, encoderISR, RISING); //External Interrupt Request (Pin 2), on posedge of pulse
    Serial.begin(9600);
}

void loop() {
    Serial.println(ctr);
}

void encoderISR() {
    if (digitalRead(encoder0A) == digitalRead(encoder0B)) {
        ctr--;
    } else {
        ctr++;
    }
}
