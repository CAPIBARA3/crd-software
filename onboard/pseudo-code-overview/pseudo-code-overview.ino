#include <Adafruit_FRAM_SPI.h>

#define MAX_FRAM_SIZE (19 * 512 * 1024)  // Total size for 19 FRAM chips
#define PACKET_SIZE 8  // Size of each data packet
#define MARKER 0xAA  // Marker for valid entry
#define VOLTAGE_PIN A0  // Analog pin for voltage reading
#define VOLTAGE_THRESHOLD 512  // Set your threshold value here (0-1023 for 10-bit ADC)

// Define chip select pins for each FRAM chip
const int CS_PINS[19] = {
  10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
  20, 21, 22, 23, 24, 25, 26, 27, 28, 29
};

Adafruit_FRAM_SPI frams[19];  // Array of FRAM objects
uint32_t fram_addr = 0;

// Setting up FRAM
void setup() {
  for (int i = 0; i < 19; i++) {
    frams[i] = Adafruit_FRAM_SPI(CS_PINS[i]);
    frams[i].begin();
  }
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

    // Determine which FRAM chip to write to
    int fram_index = fram_addr / (512 * 1024);  // Each FRAM chip has 512 KB
    uint32_t local_addr = fram_addr % (512 * 1024);  // Local address within the selected FRAM chip

    // Wrap around if we reach the end of the total FRAM size
    if (fram_addr >= MAX_FRAM_SIZE - PACKET_SIZE) {
      fram_addr = 0;  // Reset address to start
    }

    // Store the packet in the selected FRAM chip
    frams[fram_index].write(local_addr, packet, PACKET_SIZE);
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