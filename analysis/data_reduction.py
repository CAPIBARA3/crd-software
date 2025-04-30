# pseudo-code for the data reduction of the CR instrument (CAPICR)
# The code assumes data is received in raw '.bin' file format.
# And each entrance is 16 bytes long, see onboard software saving for data structure.

import struct

def compute_crc(data):
    crc = 0
    for b in data:
        crc ^= b
    return crc

def parse_packet(packet):
    if len(packet) != 8:
        return None

    marker = packet[0]
    if marker != 0xAA:
        return None

    timestamp = int.from_bytes(packet[1:5], 'little')
    adc = int.from_bytes(packet[5:7], 'little')
    crc = packet[7]
    calc_crc = compute_crc(packet[:7])

    if crc != calc_crc:
        return None  # Corrupted packet

    return {"timestamp": timestamp, "adc": adc}

def read_fram_binary(filename):
    entries = []
    with open(filename, "rb") as f:
        while True:
            block = f.read(16)
            if len(block) < 16:
                break
            primary = block[:8]
            backup = block[8:]

            result = parse_packet(primary)
            if result is None:
                result = parse_packet(backup)

            if result is not None:
                entries.append(result)
            else:
                entries.append({"timestamp": None, "adc": None})  # corrupted block

    return entries

# Example usage:
data = read_fram_binary("fram_dump.bin")

# Print result
for i, entry in enumerate(data):
    if entry["timestamp"] is None:
        print(f"Entry {i}: CORRUPTED")
    else:
        print(f"Entry {i}: Time={entry['timestamp']} ms, ADC={entry['adc']}")