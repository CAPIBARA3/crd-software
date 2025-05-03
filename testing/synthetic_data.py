import struct
import time
import random

def calculate_crc(data):
    """Calculate CRC-8 using XOR for the given data."""
    crc = 0
    for byte in data:
        crc ^= byte
    return crc

def create_packet(marker, timestamp, adc_reading):
    # Pack the data into bytes
    data = struct.pack('<B I H', marker, timestamp, adc_reading)  # Use little-endian
    # Calculate CRC-8
    crc = calculate_crc(data)
    # Return full 8-byte packet
    return data + bytes([crc])

def create_binary_file(filename, num_entries=10):
    with open(filename, 'wb') as f:
        for _ in range(num_entries):
            # Marker
            marker = 0xAA
            
            # Timestamp (4-byte millis value, wrapped to 32 bits)
            timestamp = int(time.time() * 1000) % (2**32)  # Current ms wrapped to 32 bits
            
            # ADC reading (2-byte voltage value, 10-bit ADC)
            adc_reading = random.randint(0, 1023)  # Random value between 0 and 1023
            
            # Create primary packet
            primary_packet = create_packet(marker, timestamp, adc_reading)
            
            # Create backup packet (can be same or slightly different)
            # For testing, let's create a backup with adc_reading incremented by 1 (mod 1024)
            backup_adc = (adc_reading + 1) % 1024
            backup_packet = create_packet(marker, timestamp, backup_adc)
            
            # Write the complete entry to the file (8 bytes for primary + 8 bytes for backup)
            f.write(primary_packet + backup_packet)

# Create a binary file with 100 entries
create_binary_file('./testing/data.bin', 100)
