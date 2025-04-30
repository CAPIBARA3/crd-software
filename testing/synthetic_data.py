import struct
import time
import random

def calculate_crc(data):
    """Calculate CRC-8 using XOR for the given data."""
    crc = 0
    for byte in data:
        crc ^= byte
    return crc

def create_binary_file(filename, num_entries=10):
    with open(filename, 'wb') as f:
        for _ in range(num_entries):
            # Marker
            marker = 0xAA
            
            # Timestamp (4-byte millis value, wrapped to 32 bits)
            timestamp = int(time.time() * 1000) % (2**32)  # Current ms wrapped to 32 bits
            
            # ADC reading (2-byte voltage value, 10-bit ADC)
            adc_reading = random.randint(0, 1023)  # Random value between 0 and 1023
            
            # Pack the data into bytes
            data = struct.pack('<B I H', marker, timestamp, adc_reading)  # Use little-endian
            
            # Calculate CRC-8
            crc = calculate_crc(data)
            
            # Write the complete entry to the file (8 bytes for primary + 8 bytes for backup)
            f.write(data + bytes([crc]) + bytes(7))  # Fill the rest with zeros for backup

# Create a binary file with 100 entries
create_binary_file('data.bin', 100)