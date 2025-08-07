import sys
import re
import string
import os

def is_printable(byte):
    return chr(byte) in string.printable and byte != 0x0A and byte != 0x0D

def save_payload(uuid_str, sei_data):
    filename = f"sei_{uuid_str.replace('-', '')}.bin"
    with open(filename, "wb") as f:
        f.write(sei_data)
    print(f"  Saved payload to: {filename}")

def find_sei_uuids(filename):
    with open(filename, 'rb') as f:
        data = f.read()

    # Buscar start codes 0x000001 o 0x00000001
    pattern = re.compile(b'\x00{2,3}\x01')
    matches = list(pattern.finditer(data))

    # Lista de UUIDs conocidos (tentativos HDR Vivid)
    known_uuids = {
        "aa2a8d0b-844f-93e4-c410-5d826305000a": "HDR Vivid (unconfirmed)",
        "b02c0ccb-d4c5-9164-c410-5bef62bf000a": "HDR Vivid (unconfirmed)",
        "afabeccb-d245-f17c-c410-5c0062c4000a": "HDR Vivid (unconfirmed)",
        "b1ac6cab-f8c1-1044-c410-5b5b6290000a": "HDR Vivid (unconfirmed)",
        "b1ac6cab-f8c1-1044-c410-5b5b6291000a": "HDR Vivid (unconfirmed)",
    }

    uuids_found = []

    for i in range(len(matches) - 1):
        start = matches[i].end()
        end = matches[i + 1].start()
        nal_unit = data[start:end]

        if not nal_unit:
            continue

        nal_header = nal_unit[0]
        nal_type = (nal_header >> 1) & 0x3F

        if nal_type == 39:  # SEI prefix
            payload = nal_unit[1:]
            index = 0

            while index + 1 < len(payload):
                payload_type = 0
                while payload[index] == 0xFF:
                    payload_type += 255
                    index += 1
                payload_type += payload[index]
                index += 1

                payload_size = 0
                while payload[index] == 0xFF:
                    payload_size += 255
                    index += 1
                payload_size += payload[index]
                index += 1

                if payload_type == 5:  # user_data_unregistered
                    uuid_data = payload[index : index + 16]
                    uuid_str = "-".join([
                        uuid_data[:4].hex(),
                        uuid_data[4:6].hex(),
                        uuid_data[6:8].hex(),
                        uuid_data[8:10].hex(),
                        uuid_data[10:16].hex()
                    ])
                    sei_data = payload[index + 16 : index + payload_size]

                    name = known_uuids.get(uuid_str.lower(), "Unknown")

                    print(f"\nUUID: {uuid_str} ({name})")
                    print("  Raw data (hex):", sei_data.hex()[:100], "...")
                    printable = ''.join([chr(b) if is_printable(b) else '.' for b in sei_data])
                    print("  ASCII (preview):", printable[:100])

                    save_payload(uuid_str, sei_data)

                    if uuid_str not in uuids_found:
                        uuids_found.append(uuid_str)

                index += payload_size

    if not uuids_found:
        print("No UUIDs found in the file.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_sei_uuid.py input.hevc")
        sys.exit(1)

    if not os.path.isfile(sys.argv[1]):
        print(f"File not found: {sys.argv[1]}")
        sys.exit(1)

    find_sei_uuids(sys.argv[1])
