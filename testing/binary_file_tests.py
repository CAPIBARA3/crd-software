def get_data(file_path="data.bin"):
    with open(file_path, 'rb') as file:
        data = file.read()
        return data

def get_file_size(file_path="data.bin"):
    with open(file_path, 'rb') as file:
        data = file.read()
        size_in_bytes = len(data)
        size_in_bits = size_in_bytes * 8
        return size_in_bytes, size_in_bits    

def count_0xaa_entries(data=get_data()):
    ax00_count = 0
    for i in range(0, len(data), 2):
        if data[i:i+2] == b'0xAA':
            ax00_count += 1
    return ax00_count

def compute_crc(data):
    crc = 0
    for b in data:
        crc ^= b
    return crc

def check_crc(data):
    crc = compute_crc(data)
    if crc == 0:
        return True
    else:
        return False

def check_size(size):
    if size == 0:
        return False
    if size % 16 == 0:
        return True
    else:
        return False