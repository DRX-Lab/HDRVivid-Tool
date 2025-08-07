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

## Notes

This project is a conceptual implementation inspired by [dovi\_tool](https://github.com/quietvoid/dovi_tool), adapted specifically for HDR Vivid, the Chinese HDR format.

Please be advised that this tool is currently experimental and may not function correctly in all scenarios. The implementation is subject to errors and inaccuracies.

Contributions and assistance to improve the tool are welcomed.

---

## Requirements

* Python 3.x

---
