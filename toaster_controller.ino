
#define DIV 4096
#define OUT1 A3
#define IN1 7

long sum_value= 0;
long  sensor_value =0;
double temp =0;
int i = 0;
volatile int zero_cross =0;

int period=32;
int delay1 =0;
int inByte = 0;
unsigned long time =0;

void setup() {
  // initialize serial communication at 9600 bits per second:

  pinMode(OUT1, OUTPUT);
  pinMode(IN1, INPUT);
  attachInterrupt(4, zero, HIGH);
  analogReference(EXTERNAL);
  Serial.begin(9600);
  
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  
  sum_value += analogRead(A1);
  if (i>DIV) {
    sensor_value = map(sum_value/128,0,1023*(DIV/128),0,4096);
    temp = sensor_value/10.0;
    sum_value = 0;    
    i=0;
    Serial.println(temp);
  }
  i++;  
  
  
  if(zero_cross>=period-delay1){
      digitalWrite(OUT1, HIGH); 
      if(zero_cross>=period) {
        digitalWrite(OUT1,LOW);
       zero_cross=0; 
    }
  }

    if (Serial.available() > 0) {
        //get incoming byte
        inByte = Serial.read();
    
        if(inByte>period)
            inByte = period;
        delay1= inByte;
        }

}

void zero()
{
  zero_cross++; 
}


