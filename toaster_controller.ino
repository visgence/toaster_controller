/*
 * Toaster Oven Controller
 * Sending a '%' will print current temperature in C
 * Sending a value 0x0 to 0x32 (period) will set PWM value
 * Visgence Inc
 * Evan Salazar (evan@visgence.com)

 */
#define DIV 1024
#define OUT1 3
#define IN1 2

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
  attachInterrupt(0, zero, HIGH);
  Serial.begin(9600);
  
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  
  sum_value += analogRead(A0);

  if (i>DIV) {
    //sensor_value = map(sum_value/DIV,0,1023,0,50000);
    //temp = sensor_value/100.0;
    temp = sum_value * 500.0 / (1023.0*DIV);
    sum_value = 0;    
    i=0;
    //Serial.println(temp);
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
        
        //Print temp if we get a "%"
        
        if(inByte == '%')
            Serial.println(temp);

        else if(inByte>period)
            inByte = period;
        
        else
            delay1= inByte;
        }

}

void zero()
{
  zero_cross++; 
}


