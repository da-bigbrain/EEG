int soundCard = A0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(2000000);
  Serial.println("Starting...");
  pinMode(soundCard, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  int alphaData = analogRead(soundCard);
  // Serial.print("data = ");
  Serial.println(alphaData);
}
