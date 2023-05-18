  const int GSR=A2;
  int sensorValue=0;
  int gsr_average=0;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  // print current time
  //Serial.print("Start from Arduino!");
  //Serial.println();
}

void loop() {
  // put your main code here, to run repeatedly:
  long sum=0;
  for(int i=0;i<10;i++){
    sensorValue=analogRead(GSR);
    sum += sensorValue;
    delay(5);
  }
  gsr_average= sum/10;
  Serial.println(gsr_average);
}
