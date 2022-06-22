/*
  This example reads audio data from the on-board PDM microphones, and prints
  out the samples to the Serial console. The Serial Plotter built into the
  Arduino IDE can be used to plot the audio data (Tools -> Serial Plotter)

  Circuit:
  - Arduino Nano 33 BLE board, or
  - Arduino Nano RP2040 Connect, or
  - Arduino Portenta H7 board plus Portenta Vision Shield

  This example code is in the public domain.
*/

#include <PDM.h>

// default number of output channels
static const char channels = 1;

// default PCM output frequency
static const int frequency = 16000;

// Buffer to read samples into, each sample is 16-bits
uint16_t sampleBuffer[2048];
uint8_t sampleBuffer_8bit[6200];
int sb_index = 0;

// Number of audio samples read
volatile int samplesRead;

void setup() {
  SerialUSB.begin(115200);
  while(!SerialUSB);

  // Configure the data receive callback
  PDM.onReceive(onPDMdata);

  // Optionally set the gain
  // Defaults to 20 on the BLE Sense and 24 on the Portenta Vision Shield
   PDM.setGain(127);

  // Initialize PDM with:
  // - one channel (mono mode) 
  // - a 16 kHz sample rate for the Arduino Nano 33 BLE Sense
  // - a 32 kHz or 64 kHz sample rate for the Arduino Portenta Vision Shield
  if (!PDM.begin(channels, frequency)) {
    SerialUSB.println("Failed to start PDM!");
    while (1);
  }
}

void loop() {
  // Wait for samples to be read
  
  if (samplesRead) {

    for (int i = 0; i < samplesRead; i=i+1) {

      sampleBuffer_8bit[sb_index] = '\n';
      sb_index ++;
      sampleBuffer_8bit[sb_index] = (sampleBuffer[i] >> 8) & 0xFF;
      sb_index ++;
      sampleBuffer_8bit[sb_index] = (sampleBuffer[i] & 0xFF);
      sb_index ++;

  }

    if (sb_index >= 6144){
 
        SerialUSB.write(sampleBuffer_8bit,sb_index);
 
        sb_index=0;
        }
        
    // Clear the read count
    samplesRead = 0;
  }
}

/**
 * Callback function to process the data from the PDM microphone.
 * NOTE: This callback is executed as part of an ISR.
 * Therefore using `Serial` to print messages inside this function isn't supported.
 * */
 
void onPDMdata() {
  // Query the number of available bytes
  int bytesAvailable = PDM.available();

  // Read into the sample buffer
  PDM.read(sampleBuffer, bytesAvailable);

  // 16-bit, 2 bytes per sample
  samplesRead = bytesAvailable / 2;

}
