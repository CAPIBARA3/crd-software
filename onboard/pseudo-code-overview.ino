// This code is for an Arduino-based system that reads voltage from an analog pin, and stores it to the FRAM memory.

// The data structure is:
// | Byte(s) | Field  Description |
// | --- | --- | --- |
// | 1 | Marker (`0xAA`) | Identifies a valid entry start |
// | 2–5 | Timestamp | 4-byte `millis()` value |
// | 6–7 | ADC reading | 2-byte voltage value (10-bit ADC) |
// | 8 | CRC-8 | XOR of previous 7 bytes |

#include <Adafruit_FRAM_SPI.h>

Adafruit_FRAM_SPI fram = Adafruit_FRAM_SPI(CS_PIN);
uint32_t fram_addr = 0;


// setting up FRAM
void setup() {
  fram.begin();
}

void loop() {
  uint16_t voltage = analogRead(A0);
  uint32_t timestamp = millis();

  uint8_t packet[8];
  packet[0] = 0xAA;
  memcpy(&packet[1], &timestamp, 4);
  memcpy(&packet[5], &voltage, 2);
  packet[7] = compute_crc(packet, 7);

  // Store twice for redundancy
  for (int copy = 0; copy < 2; copy++) {
    for (int i = 0; i < 8; i++) {
      fram.write8(fram_addr++, packet[i]);
    }
  }

  delay(1000);  // Or only write when there's a detection (reducing data size)
}

// CRC is a test to detect data corruption
uint8_t compute_crc(uint8_t *data, int len) {
  uint8_t crc = 0;
  for (int i = 0; i < len; i++) {
    crc ^= data[i];  // Simple XOR checksum
  }
  return crc;
}
