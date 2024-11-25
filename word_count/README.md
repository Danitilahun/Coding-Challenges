# Command-line Word Counter Tool (ccwc)

## Overview

`ccwc` is a Python-based command-line tool that counts lines, words, characters, or bytes in a file or standard input. It mimics the functionality of Unix `wc` with additional flexibility.

## Features

- Count **lines**, **words**, **characters**, and **bytes**.
- Process **file input** or **standard input**.
- Modular design for easy maintenance and extension.

## Installation

1. Ensure Python 3.7 or later is installed on your system.
2. Clone or download this repository.
3. Save the script files in the desired directory.

## Usage

### Running the Script

To use the `ccwc.py` script, run:

```bash
python ccwc.py [options] [filename]
```

### Options

| Option    | Description                                |
|-----------|--------------------------------------------|
| `-l`      | Count the number of lines in the input.    |
| `-w`      | Count the number of words in the input.    |
| `-m`      | Count the number of characters.           |
| `-c`      | Count the number of bytes.                |

### Examples

#### Count lines in a file:
```bash
python ccwc.py -l test.txt
```

#### Count words from standard input:
```bash
cat test.txt | python ccwc.py -w
```

#### Count bytes, characters, words, and lines in a file:
```bash
python ccwc.py -c -m -w -l test.txt
```

#### Default behavior (counts all metrics):
```bash
python ccwc.py test.txt
```

### Batch Script (Windows)

To simplify running the script on Windows, use the provided batch file:

#### Save the batch file as `ccwc.bat`:
```batch
@echo off
python "C:\Users\<Path>\ccwc.py" %*
```

Replace `<Path>` with the actual path to your `ccwc.py` file.

#### Run with:
```cmd
ccwc -l test.txt
```

## File Structure

- `ccwc.py`: Main script for argument parsing and execution.
- `ccwc_utils.py`: Utility functions for counting lines, words, characters, and bytes.

## Dependencies

- Python 3.7 or later