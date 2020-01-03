#include "Wire.h" //Arduino I2C library
#define MPU_ADDR 0x68 // I2C address of MPU-6050

int16_t ax, ay, az; //raw data (MPU-6050 has 16 bit ADC)

void setup() {
    Serial.begin(9600);
    Wire.begin();
    Wire.beginTransmission(MPU_ADDR);
    Wire.write(0x6B); //register PWR_MGMT_1
    Wire.write(0); //wake up
    Wire.endTransmission(true);
    Wire.beginTransmission(MPU_ADDR);
    Wire.write(0x1C); //register AFS_SEL
    Wire.write(0b00000000); //full scale range +/- 2g (reading of 1g = 2^(16-2) = 16384)
    Wire.endTransmission(true);
}

void loop() {
    Wire.beginTransmission(MPU_ADDR);
    Wire.write(0x3B); //start with register 0x3B (ACCEL_XOUT_H)
    Wire.endTransmission(false); //false ==> sends a restart message after transmission, the bus will not be released
    Wire.requestFrom(MPU_ADDR, 6, true); //request from 6 registers; true ==> send a stop message after the request, releasing the bus

    //For register locations, look at the MPU-6000/MPU-6050 Register Map, page 7
    ax = Wire.read() << 8 | Wire.read(); //(0x3B (ACCEL_XOUT_H) << 8) OR (0x3C (ACCEL_XOUT_L))
    ay = Wire.read() << 8 | Wire.read(); //(0x3D (ACCEL_YOUT_H) << 8) OR (0x3E (ACCEL_YOUT_L))
    az = Wire.read() << 8 | Wire.read(); //(0x3F (ACCEL_ZOUT_H) << 8) OR (0x40 (ACCEL_ZOUT_L))

    Serial.print("aX=");
    Serial.print(ax);
    Serial.print(" aY=");
    Serial.print(ay);
    Serial.print(" aZ=");
    Serial.print(az);
    Serial.println();

    //delay(200);
}
