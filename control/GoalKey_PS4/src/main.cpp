#include <PS4Controller.h>
#include <Arduino.h>

unsigned long lastTimeStamp = 0;

#define PI 3.1415926536
int rightwheel[2]={12,14},leftwheel[2]={27,26},output[3],front[2]={23,22};
int rawvalx,rawvaly;



void out(int rawval, int pin[2]){
  int x;
  x=pin[0]==12?0:(pin[0]==27?1:2);
  if(rawval>0){ 
    digitalWrite(pin[1],1);
    ledcWrite(x,rawval);
  }
  else{
    digitalWrite(pin[1],0);
    ledcWrite(x,-rawval);
  }

}
void differential(int x,int y,int output[]){
  float z = sqrt(x * x + y * y);
  float rad = atan2(y,x);
  float angle = rad * 180 /PI;
  //Serial.print("angle:");Serial.println(angle);

    if(angle>90)
    {
      angle = 450 - angle;
    }
    else
    {
      angle = 90 - angle;
    }

    angle = (angle*PI)/180.0; //degrees to radians
    float wheel_angles[3]={(90 * PI) / 180.0, (225 * PI) /180.0, (315 * PI) /180.0};

    for(int i=0; i < 3;i++){
         float wv = z*sin(angle)*sin(wheel_angles[i])+z*cos(angle)*cos(wheel_angles[i]);
         output[i] = wv;
    }
    output[1]=-output[1];
    output[2]=-output[2];
}


void notify()
{  
  if (millis() - lastTimeStamp > 20)
  {
    rawvalx=PS4.LStickX()*2;
    rawvaly=PS4.LStickY()*2;


    if(PS4.Down()){
      rawvalx=0;
      rawvaly=-255;
    }
    if(PS4.Up()){
      rawvalx=0;
      rawvaly=255;
    }
      if(PS4.Left()){
      rawvalx=-255;
      rawvaly=0;
    }
      if(PS4.Right()){
      rawvalx=255;
      rawvaly=0;
    }
  


  //Only needed to print the message properly on serial monitor. Else we dont need it.

    differential(rawvalx,rawvaly,output);
    output[0]=output[0]>255?0:output[0];
    if(PS4.L1()){
      output[0]=255;
      output[1]=-255;
      output[2]=-255;
    }
    if(PS4.R1()){
      output[0]=-255;
      output[1]=255;
      output[2]=255;
    }
    out(output[0],front);
    out(output[1],leftwheel);
    out(output[2],rightwheel);
    Serial.print(output[0]);Serial.print(",");Serial.print(output[1]);Serial.print(",");Serial.println(output[2]);  
    lastTimeStamp = millis();
  }


}

void onConnect()
{
  Serial.println("Connected!.");
}

void onDisConnect()
{
  Serial.println("Disconnected!.");    
}

const int freq = 5000;
const int resolution = 8;

void setup() 
{
  Serial.begin(115200);
  ledcSetup(0, freq, resolution);
  ledcSetup(1, freq, resolution);
  ledcSetup(2, freq, resolution);
  ledcAttachPin(12, 0);
  pinMode(14,OUTPUT);
  ledcAttachPin(27, 1);
  pinMode(26,OUTPUT);
  ledcAttachPin(23, 2);
  pinMode(22,OUTPUT);
  
  PS4.attachOnConnect(onConnect);
  PS4.attachOnDisconnect(onDisConnect);
  PS4.begin();
  PS4.attach(notify);
  Serial.println("Ready.");
}

void loop() 
{

}