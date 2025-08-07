# HDRVivid-Tool

A utility for extracting and injecting HDR Vivid SEI metadata from HEVC (.hevc/.h265) video files.

---

## Features

- **Extraction**: Extract full HDR Vivid SEI metadata from an HEVC file into a binary `.bin` file.
- **Injection**: Inject HDR Vivid SEI metadata from a `.bin` file back into an HEVC video stream.

---

## Usage

Extract HDR Vivid SEI metadata to a `.bin` file:

```bash
python hdrvivid_tool.py -i input.hevc --extract-bin
````

Inject HDR Vivid SEI metadata from a `.bin` file into an HEVC file:

```bash
python hdrvivid_tool.py -i input.hevc --inject-bin hdr_vivid_full.bin -o output.hevc
```

---

## Command Line Arguments

| Option                | Description                                      | Required                                |
| --------------------- | ------------------------------------------------ | --------------------------------------- |
| `-i`, `--input`       | Input HEVC file (.hevc or .h265)                 | Yes                                     |
| `-e`, `--extract-bin` | Extract HDR Vivid SEI metadata to a `.bin` file  | No (mutually exclusive with injection)  |
| `-j`, `--inject-bin`  | Inject HDR Vivid SEI metadata from a `.bin` file | No (mutually exclusive with extraction) |
| `-o`, `--output`      | Output file path when injecting SEI metadata     | Required when injecting                 |

---

## Important Note About Test Files

## Notes

This project is a conceptual and experimental implementation inspired by [dovi_tool](https://github.com/quietvoid/dovi_tool), adapted specifically for HDR Vivid, the Chinese HDR format.

Please be advised that this tool may not function correctly in all scenarios and is subject to errors and inaccuracies.

The files `test_hdrvivid.hevc` and `test_hdr.hevc` represent the same base video content with one key difference:

- `test_hdrvivid.hevc` is the original video file **containing HDR Vivid SEI metadata**.
- `test_hdr.hevc` is a version where the HDR Vivid SEI metadata has been **removed for testing purposes**.

This setup is intended solely for testing and demonstration purposes, allowing users to **extract** the HDR Vivid metadata from `test_hdrvivid.hevc` and **inject** it into `test_hdr.hevc`, thereby illustrating how the extraction and injection functionalities of this tool are expected to operate.

Any contributions, suggestions, or assistance to improve or complete the tool are highly appreciated.

---

## Requirements

* Python 3.x

---
