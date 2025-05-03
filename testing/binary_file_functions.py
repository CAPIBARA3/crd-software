import os

def get_data(file_path):
    """Read binary data from a file."""
    # Ensure the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    with open(file_path, 'rb') as file:
        data = file.read()
        return data

def check_not_empty(filename):
    """Check if the binary data is not empty."""
    data = get_data(filename)
    if len(data) == 0:
        raise ValueError("The binary data is empty.")
    else:
        return True

def get_file_size(filename):
    """Get the size of the binary data in bytes and bits."""
    data = get_data(filename)
    if check_not_empty(filename):
        size_in_bytes = len(data)
        size_in_bits = size_in_bytes * 8
        return size_in_bytes, size_in_bits

def count_0xaa_entries(filename):
    """Count the number of 0xaa entries in the binary data."""
    data = get_data(filename)
    if check_not_empty(filename):
        aa_count = 0
        # Count complete 16-byte entries
        for i in range(0, len(data), 16):
            if i + 8 <= len(data) and data[i] == 0xAA:  # Check for marker in the primary packet
                aa_count += 1
        return aa_count

def compute_crc(filename):
    """Compute CRC-8 using XOR for the given data."""
    data = get_data(filename)
    crc = 0
    for b in data:
        crc ^= b
    return crc

def check_crc(filename):
    """Check if the CRC-8 of each 16-byte entry is valid."""
    data = get_data(filename)
    if check_not_empty(data):
        for i in range(0, len(data), 16):
            if i + 8 <= len(data):  # Ensure there's a full entry
                entry = data[i:i+16]
                primary = entry[:8]
                crc = primary[7]
                calc_crc = compute_crc(primary[:7])
                if crc != calc_crc:
                    return False  # Found a corrupted entry
        return True
    return False

def check_size(filename): # size in bytes
    """Check if the file size is a multiple of 16 = 2 x 8."""
    size = get_file_size(filename)[0]
    if size == 0:
        return False
    if size % 16 == 0:
        return True
    else:
        return False
    




# create synthetic data for testing
import random
import struct
import time

def create_synthetic_data(filename, num_entries):
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
    
    create_binary_file(filename, num_entries)