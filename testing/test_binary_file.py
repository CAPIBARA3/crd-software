import os
import pytest
import binary_file_functions as bff

# for synthetic data generation
import struct
import time
import random

filename = 'temp_file.bin'
num_entries = 100
num_bytes = num_entries * 8 * 2 # 8 byte packets stores twice
data = b''

def test_create_synthetic_data():
    """Create a synthetic binary file for testing."""
    bff.create_synthetic_data(filename, num_entries)
    assert os.path.exists(filename), f"Failed to create synthetic data file {filename}."

def test_get_data():
    data = bff.get_data(filename)
    assert len(data) == num_bytes, f"Expected {num_bytes} entries, got {len(data)}"

def test_check_not_empty():
    assert bff.check_not_empty(filename), "Data should not be empty"

def test_get_file_size():
    size = bff.get_file_size(filename)
    assert size == (num_bytes, num_bytes*8), f"Expected size 1024, got {size}"

def test_count_0xaa_entries():
    count = bff.count_0xaa_entries(filename)
    assert count == num_entries, f"Expected 0xAA entries: {num_entries}, got {count}"

def test_compute_crc():
    assert bff.compute_crc(filename) == 0, "CRC computation failed"

def test_check_size():
    statement = bff.check_size(filename)
    assert statement == True

def test_remove_temp_file():
    os.remove(filename)
    assert not os.path.exists(filename), f"Temporary file {filename} was not removed."