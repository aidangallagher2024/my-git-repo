// Pin definitions for the rotary encoder
const int encoderPinA = 2; // Encoder output A (to pin 2)
const int encoderPinB = 3; // Encoder output B (to pin 3)
volatile int impulseCount = 0;  // Variable to count the number of impulses
const int impulsesPerTurn = 600; // 600 impulses per complete turn
float turns = 0.0;  // Variable to track complete turns
int Turn2;
unsigned long previousMillis = 0; // Timer variable
const long interval = 1000;       // Interval for 1 second (1000 milliseconds)

void setup() {
  // Initialize the encoder pins as inputs
  pinMode(encoderPinA, INPUT_PULLUP);
  pinMode(encoderPinB, INPUT_PULLUP);
  pinMode(13, OUTPUT);      // set LED pin as output, used for notifying serial communication
  digitalWrite(13, LOW);    // switch off LED pin
  pinMode(5, OUTPUT); 
  digitalWrite(5, LOW);
  // Attach interrupts to the encoder pins
  attachInterrupt(digitalPinToInterrupt(encoderPinA), countImpulse, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoderPinB), countImpulse, CHANGE);
   // Initialize serial communication for debugging
  Serial.begin(115200);   //match jetson baud rate
  }
  
void loop() {
  // Check if 1 second has passed
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    // Calculate the number of turns
    turns = (float)impulseCount / impulsesPerTurn;
    // Print the number of turns per second
    //Serial.print("Turns per second: ");
    //Serial.println(turns);
    // Reset the impulse count for the next second
    impulseCount = 0;
    Turn2 = turns * 100;
    if (Turn2 > 749){
      //digitalWrite(5,HIGH);
      digitalWrite(13,HIGH);

            }
    else{
      //digitalWrite(5,LOW);
      digitalWrite(13,LOW);

      }
    }
    
    if (Serial.available()) 
    {
    char data_rcvd = Serial.read();   // read one byte from serial buffer and save to data_rcvd

    if (data_rcvd == '1') digitalWrite(13, HIGH); // switch LED On
    if (data_rcvd == '0') digitalWrite(13, LOW);  // switch LED Off
     }  
     if (Turn2 > 99){
      //digitalWrite(5,HIGH);
      //digitalWrite(13,HIGH);
      Serial.write('1');
      }
    else{
      //digitalWrite(5,LOW);
      //digitalWrite(13,LOW);
      Serial.write('0');
     
   }
   delay(200);
}
    
void countImpulse() {
  // Increment the impulse count each time a change is detected on either pin
  impulseCount++;}
