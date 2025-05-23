#include <RTTStream.h>
RTTStream rtt;

// JOYSTICK PORTS
// STK_A:   PA07 => 9
// STK_B:   PA08 => 4
// STK_C:   PA09 => 3
// STK_D:   PA10 => 1
// STK_CEN: PA11 => 0

int BTTNS   = 3;
int STK_A   = 9;
int STK_B   = 4;
int STK_C   = 3;
int STK_D   = 1;
int STK_CEN = 0;

int idx = 0;
int avg = 0;
int last_avg = 0;

void setup()
{
  pinMode(BTTNS, INPUT);
  pinMode(STK_A, INPUT);
  pinMode(STK_B, INPUT);
  pinMode(STK_C, INPUT);
  pinMode(STK_D, INPUT);
  pinMode(STK_CEN, INPUT);
  rtt.println("HCI PCB");
}

void loop(){
  idx++;
  int test = analogRead(STK_A);
  avg += test;
  if (idx == 10){
    last_avg = avg/10;
    avg = 0;
    idx = 0;
  }
  rtt.println(last_avg - last_avg%10);
}