#include <RTTStream.h>
RTTStream rtt;

void setup()
{
  pinMode(13, OUTPUT);
  pinMode(3, INPUT);
  rtt.println("HCI PCB");
}

void loop()
{
  int test = analogRead(3);
  rtt.write("HELLO PYTHON");
  rtt.println("HELLO AGAIN");
  // while (rtt.available()) {
  //   rtt.write("samd received: ");
  //   rtt.write(rtt.read());
  //   rtt.write(test);
  //   rtt.write("\n");
  // }
}