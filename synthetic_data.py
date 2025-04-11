import struct
import time
import random

def calculate_crc(data):
    """Calculate CRC-8 using XOR for the given data."""
    crc = 0
    for byte in data:
        crc ^= byte
    return crc

def create_binary_file(filename, num_entries):
    with open(filename, 'wb') as f:
        for _ in range(num_entries):
            # Marker
            marker = 0xAA
            
            # Timestamp (4-byte millis value)
            timestamp = int(time.time() * 1000)  # Current time in milliseconds
            
            # ADC reading (2-byte voltage value, 10-bit ADC)
            adc_reading = random.randint(0, 1023)  # Random value between 0 and 1023
            
            # Pack the data into bytes
            data = struct.pack('>B I H', marker, timestamp, adc_reading)
            
            # Calculate CRC-8
            crc = calculate_crc(data)
            
            # Write the complete entry to the file
            f.write(data + bytes([crc]))

# Create a binary file with 10 entries
create_binary_file('data.bin', 10)