import os
import pytest
import binary_file_tests as bft

# for synthetic data generation
import struct
import time
import random

filename = './testing/temp_test.bin'
num_entries = 100

def create_synthetic_data(filename, num_entries=10):
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
    assert os.path.exists(filename), f"Failed to create synthetic data file {filename}."


def test_get_data():
    data = bft.get_data(filename)
    assert len(data) == num_entries, f"Expected {num_entries} entries, got {len(data)}"
    for entry in data:
        assert entry['timestamp'] is not None, "Timestamp should not be None"
        assert entry['adc'] is not None, "ADC value should not be None"

def test_check_not_empty():
    data = bft.get_data(filename)
    assert len(data) > 0, "Data should not be empty"

def test_get_file_size():
    size = bft.get_file_size(filename)
    assert size == num_entries*8*2, f"Expected size 1024, got {size}"

def test_count_0xaa_entries():
    count = bft.count_0xaa_entries(filename)
    assert count == num_entries, f"Expected 0xAA entries: {num_entries}, got {count}"

def test_compute_crc():
    continue
    # data = bft.get_data(filename)
    # for entry in data:
    #     packet = struct.pack('<B I H', 0xAA, entry['timestamp'], entry['adc'])
    #     crc = bft.compute_crc(packet)
    #     assert crc == entry['crc'], f"CRC mismatch for entry {entry}"

def test_check_size():
    statement = bft.get_file_size(filename)
    assert statement == True

def test_remove_temp_file():
    os.remove(filename)
    assert not os.path.exists(filename), f"Temporary file {filename} was not removed."