from colorama import Fore, Style, init
import argparse

init(autoreset=True)

def find_start_codes(data):
    start_codes = []
    i = 0
    while i < len(data) - 4:
        if data[i:i+3] == b'\x00\x00\x01':
            start_codes.append(i)
            i += 3
        elif data[i:i+4] == b'\x00\x00\x00\x01':
            start_codes.append(i)
            i += 4
        else:
            i += 1
    return start_codes

def parse_sei_message(sei_payload):
    i = 0
    payload_type = 0
    while i < len(sei_payload):
        byte = sei_payload[i]
        i += 1
        payload_type += byte
        if byte != 0xFF:
            break

    payload_size = 0
    while i < len(sei_payload):
        byte = sei_payload[i]
        i += 1
        payload_size += byte
        if byte != 0xFF:
            break

    sei_data = sei_payload[i:i + payload_size]
    return payload_type, sei_data

def extract_hdr_vivid(data):
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Extracting HDR Vivid data...")

    start_codes = find_start_codes(data)
    start_codes.append(len(data))

    all_hdr_vivid_data = bytearray()

    for i in range(len(start_codes) - 1):
        start = start_codes[i]
        end = start_codes[i + 1]
        nal_unit = data[start:end]

        if nal_unit.startswith(b'\x00\x00\x01'):
            nal_unit = nal_unit[3:]
        elif nal_unit.startswith(b'\x00\x00\x00\x01'):
            nal_unit = nal_unit[4:]

        if not nal_unit:
            continue

        nal_header = nal_unit[0]
        nal_type = (nal_header >> 1) & 0x3F

        if nal_type == 39:  # SEI message
            sei_payload = nal_unit[2:]  # skip 2-byte header
            payload_type, sei_data = parse_sei_message(sei_payload)

            if payload_type == 137:
                all_hdr_vivid_data.extend(sei_data)

    if all_hdr_vivid_data:
        with open("hdr_vivid_full.bin", "wb") as f:
            f.write(all_hdr_vivid_data)
        print(f"{Fore.GREEN}[✓]{Style.RESET_ALL} HDR Vivid data extracted to: hdr_vivid_full.bin")
    else:
        print(f"{Fore.RED}[!]{Style.RESET_ALL} No HDR Vivid data found.")

def make_sei_nal_from_bin(bin_data, max_unit_size=255):
    nal_units = []

    i = 0
    while i < len(bin_data):
        chunk = bin_data[i:i + max_unit_size]
        i += len(chunk)

        payload_type = bytearray()
        val = 137
        while val >= 0xFF:
            payload_type.append(0xFF)
            val -= 0xFF
        payload_type.append(val)

        payload_size = bytearray()
        val = len(chunk)
        while val >= 0xFF:
            payload_size.append(0xFF)
            val -= 0xFF
        payload_size.append(val)

        sei_message = payload_type + payload_size + chunk
        nal_header = b'\x4E\x01'  # nal_unit_type = 39 (SEI), nuh_layer_id = 0, temporal_id = 1
        nal_unit = b'\x00\x00\x01' + nal_header + sei_message
        nal_units.append(nal_unit)

    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Generated SEI NAL units from bin data.")
    return nal_units

def inject_hdr_vivid(original_data, bin_file, output_file):
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Injecting HDR Vivid data...")

    try:
        with open(bin_file, "rb") as f:
            bin_data = f.read()
        print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Read bin file: {bin_file}")
    except FileNotFoundError:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} HDR Vivid bin file not found: {bin_file}")
        return

    sei_nal_units = make_sei_nal_from_bin(bin_data)

    start_codes = find_start_codes(original_data)
    start_codes.append(len(original_data))

    insert_index = 0
    for i in range(len(start_codes) - 1):
        start = start_codes[i]
        end = start_codes[i + 1]
        nal_unit = original_data[start:end]

        if nal_unit.startswith(b'\x00\x00\x01'):
            nal = nal_unit[3:]
        elif nal_unit.startswith(b'\x00\x00\x00\x01'):
            nal = nal_unit[4:]
        else:
            continue

        if not nal:
            continue

        nal_type = (nal[0] >> 1) & 0x3F
        if nal_type > 34:
            insert_index = start
            break

    final_data = bytearray()
    final_data.extend(original_data[:insert_index])
    for sei_nal in sei_nal_units:
        final_data.extend(sei_nal)
    final_data.extend(original_data[insert_index:])

    with open(output_file, "wb") as f:
        f.write(final_data)

    print(f"{Fore.GREEN}[✓]{Style.RESET_ALL} HDR Vivid data injected into: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="HDRVivid-Tool")
    parser.add_argument("-i", "--input", required=True, help="Input .hevc/.h265 file")
    parser.add_argument("-e", "--extract-bin", action="store_true", help="Extract full HDR Vivid SEI data to a .bin file")
    parser.add_argument("-j", "--inject-bin", metavar="BIN", help="Inject HDR Vivid SEI data from a .bin file")
    parser.add_argument("-o", "--output", help="Output file when injecting")
    args = parser.parse_args()

    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Starting HDRVivid-Tool...")

    try:
        with open(args.input, "rb") as f:
            data = f.read()
        print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Read input file: {args.input}")
    except FileNotFoundError:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Input file not found: {args.input}")
        return

    if args.extract_bin:
        extract_hdr_vivid(data)
    elif args.inject_bin:
        if not args.output:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} You must specify the output file using -o or --output")
            return
        inject_hdr_vivid(data, args.inject_bin, args.output)
    else:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} You must specify either --extract-bin or --inject-bin")

if __name__ == "__main__":
    main()