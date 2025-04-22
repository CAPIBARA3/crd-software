#include <Adafruit_FRAM_SPI.h>

#define CS_PIN 10  // Chip select pin for FRAM //ADJUST
#define MAX_FRAM_SIZE 32768  // Adjust based on your FRAM size //ADJUST
#define PACKET_SIZE 8  // Size of each data packet
#define MARKER 0xAA  // Marker for valid entry
#define VOLTAGE_PIN A0  // Analog pin for voltage reading //ADJUST
#define VOLTAGE_THRESHOLD 512  // Set your threshold value here (0-1023 for 10-bit ADC)

Adafruit_FRAM_SPI fram = Adafruit_FRAM_SPI(CS_PIN);
uint32_t fram_addr = 0;

// Setting up FRAM
void setup() {
  fram.begin();
  fram_addr = 0;  // Initialize address
}

void loop() {
  // Read voltage and timestamp
  uint16_t voltage = analogRead(VOLTAGE_PIN);
  uint32_t timestamp = millis();

  // Check if the voltage exceeds the threshold
  if (voltage > VOLTAGE_THRESHOLD) {
    // Create data packet
    uint8_t packet[PACKET_SIZE];
    packet[0] = MARKER;
    memcpy(&packet[1], &timestamp, 4);
    memcpy(&packet[5], &voltage, 2);
    packet[7] = compute_crc(packet, PACKET_SIZE - 1);

    // Wrap around if we reach the end of FRAM
    if (fram_addr >= MAX_FRAM_SIZE - PACKET_SIZE) {
      fram_addr = 0;  // Reset address to start
    }

    // Store the packet in FRAM
    fram.write(fram_addr, packet, PACKET_SIZE);
    fram_addr += PACKET_SIZE;  // Move to the next address
  }

  delay(1000);  // Delay between readings
}


// CRC is a test to detect data corruption
uint8_t compute_crc(uint8_t *data, int len) {
  uint8_t crc = 0;
  for (int i = 0; i < len; i++) {
    crc ^= data[i];  // Simple XOR checksum
  }
  return crc;
}
