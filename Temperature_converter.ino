
/* Lilypad Temperature Sensor reading
 * Average 10 sample temperatures and return average 
 * Output currently in Celsius
 */


void setup() {
    // initialize the serial port
    Serial.begin(9600);
}

void loop() {
    float temperature = 0.0;   // Temperature
    int sample;                // counts through samples
    float ten_samples = 0.0;   // sum of 10 samples
  
    // Take 10 readings
    for (sample = 0; sample < 10; sample++) {
        // convert reading from analog output to temperature value
        temperature = ((float)analogRead(A0) * 5.0 / 1024.0) - 0.5;
        temperature = temperature / 0.01;
        
        // take a reading to sample every 0.1 seconds
        delay(100);
        
        // sum of sample readings
        ten_samples = ten_samples + temperature;
    }
    
    // get average of smaples
    temperature = ten_samples / 10.0;
    
    // Print final temperature to serial port
    Serial.print(temperature);
    Serial.println(" degrees Celsius");

    // Reset samples
    ten_samples = 0.0;
}
