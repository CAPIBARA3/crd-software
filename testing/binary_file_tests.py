import os

def get_data(file_path="data.bin"):
    """Read binary data from a file."""
    # Ensure the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    with open(file_path, 'rb') as file:
        data = file.read()
        return data

def check_not_empty(data):
    """Check if the binary data is not empty."""
    if len(data) == 0:
        raise ValueError("The binary data is empty.")
    else:
        return True

def get_file_size(data):
    """Get the size of the binary data in bytes and bits."""
    if check_not_empty(data):
        size_in_bytes = len(data)
        size_in_bits = size_in_bytes * 8
        return size_in_bytes, size_in_bits

def count_0xaa_entries(data):
    """Count the number of 0xaa entries in the binary data."""
    if check_not_empty(data):
        aa_count = 0
        # Count complete 16-byte entries
        for i in range(0, len(data), 16):
            if i + 8 <= len(data) and data[i] == 0xAA:  # Check for marker in the primary packet
                aa_count += 1
        return aa_count

def compute_crc(data):
    """Compute CRC-8 using XOR for the given data."""
    crc = 0
    for b in data:
        crc ^= b
    return crc

def check_crc(data):
    """Check if the CRC-8 of each 16-byte entry is valid."""
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

def check_size(size):
    """Check if the file size is a multiple of 16 = 2 x 8."""
    if size == 0:
        return False
    if size % 16 == 0:
        return True
    else:
        return False

# Example usage
data = get_data("data.bin")
size_in_bytes, size_in_bits = get_file_size(data)
if check_size(size_in_bytes):
    print("File size is valid.")
else:
    print("File size is not valid.")

aa_count = count_0xaa_entries(data)
print(f"Number of 0xAA entries: {aa_count}")

if check_crc(data):
    print("All entries have valid CRC.")
else:
    print("Some entries have invalid CRC.")