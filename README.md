# TimeDcode

**Time converter for forensic professionals**

TimeDcode is a graphical application designed to decode and convert timestamps from various formats commonly encountered in digital forensics. It provides an intuitive interface for converting timestamps to human-readable dates and times across multiple timezones.

## Features

- **Multiple Timestamp Format Support**: Decode 7 different timestamp formats including Unix, Windows FILETIME, and various hex encodings
- **Single Conversion Mode**: Convert a timestamp with a known format to UTC, local time, and a target timezone
- **Guess All Formats Mode**: Automatically test all supported formats to identify valid timestamps (filtered to dates between 1970-2040)
- **Timezone Conversion**: Convert timestamps to any available timezone using the IANA timezone database
- **Selectable Output**: All decoded times are displayed in selectable fields, allowing easy copy-paste operations
- **Date Range Filtering**: Guess mode filters results to show only reasonable dates (1970-2040) to reduce false positives

## Supported Timestamp Formats

1. **Unix Seconds (Decimal)** - Standard Unix timestamp in decimal format (e.g., `1696118400`)
2. **Unix Hex 32-bit Big Endian** - Unix timestamp as 32-bit hexadecimal, big-endian byte order (e.g., `0x65000000`)
3. **Unix Hex 32-bit Little Endian** - Unix timestamp as 32-bit hexadecimal, little-endian byte order (e.g., `0x00000065`)
4. **Unix Milliseconds Hex** - Unix timestamp in milliseconds as hexadecimal (e.g., `0x18E0B2C000`)
5. **Unix Milliseconds (Decimal)** - Unix timestamp in milliseconds as decimal (e.g., `1696118400000`)
6. **Windows FILETIME Big Endian** - Windows FILETIME format (100-nanosecond intervals since 1601-01-01) as hexadecimal, big-endian
7. **Windows FILETIME Little Endian** - Windows FILETIME format as hexadecimal, little-endian

## Technical Details

### Architecture

TimeDcode is built using Python 3 with a Tkinter-based graphical user interface. The application follows an object-oriented design with a single `TimeDecoderApp` class that manages all UI components and conversion logic.

### Key Technologies

- **Programming Language**: Python 3
- **GUI Framework**: Tkinter (ttk widgets for modern styling)
- **Core Libraries**:
  - `datetime`: Date and time manipulation
  - `zoneinfo`: IANA timezone database support (Python 3.9+)
  - `tkinter`: GUI components

### UI Components

- **Entry Widgets**: Input field for timestamps (Consolas monospace font)
- **Comboboxes**: Format selection and timezone selection
- **Readonly Entry Widgets**: Display decoded times (selectable for copy-paste)
- **ScrolledText**: Scrollable results area for guess mode output

### Conversion Algorithms

#### Unix Timestamp Conversion
- Standard Unix timestamps are converted using `datetime.fromtimestamp()`
- Hex values are parsed and converted to integers before timestamp conversion
- Little-endian formats reverse byte order before conversion

#### Windows FILETIME Conversion
Windows FILETIME values are converted to Unix timestamps using the formula:
```
unix_timestamp = (filetime_value - 116444736000000000) / 10_000_000
```

Where:
- `116444736000000000` is the FILETIME value for 1970-01-01 00:00:00 UTC
- FILETIME uses 100-nanosecond intervals since 1601-01-01
- Division by 10,000,000 converts to seconds

### Input Processing

The application automatically handles various input formats:
- Strips whitespace and common prefixes (`0x`, spaces, colons)
- Pads odd-length hex strings with leading zero
- Validates date ranges to prevent unreasonable results

## Requirements

- **Python 3.9 or higher** (required for `zoneinfo` module)
- **Tkinter** (usually included with Python installations)
- **zoneinfo module** (included in Python 3.9+ standard library)

## Installation & Running Instructions

### macOS

#### Step 1: Check Python Version
Open Terminal and check if Python 3.9+ is installed:
```bash
python3 --version
```

#### Step 2: Install Python (if needed)
If Python 3.9+ is not installed, you can install it using:

**Option A: Homebrew** (recommended)
```bash
brew install python3
```

**Option B: Official Python Installer**
1. Visit [python.org/downloads](https://www.python.org/downloads/)
2. Download the latest Python 3.x installer for macOS
3. Run the installer and follow the instructions

#### Step 3: Verify Tkinter
Tkinter should be included with Python, but you can verify it's available:
```bash
python3 -m tkinter
```
If a window opens, Tkinter is installed correctly. Close the window.

#### Step 4: Run TimeDcode
Navigate to the TimeDcode directory and run:
```bash
cd /path/to/TimeDcode
python3 TimeDcode
```

### Windows

#### Step 1: Check Python Version
Open Command Prompt or PowerShell and check if Python 3.9+ is installed:
```cmd
python --version
```
or
```cmd
py --version
```

#### Step 2: Install Python (if needed)
1. Visit [python.org/downloads](https://www.python.org/downloads/)
2. Download the latest Python 3.x installer for Windows
3. Run the installer
4. **Important**: Check the box "Add Python to PATH" during installation
5. Complete the installation

#### Step 3: Verify Tkinter
Tkinter should be included with Python. Verify it's available:
```cmd
python -m tkinter
```
or
```cmd
py -m tkinter
```
If a window opens, Tkinter is installed correctly. Close the window.

#### Step 4: Run TimeDcode
Navigate to the TimeDcode directory and run:
```cmd
cd C:\path\to\TimeDcode
python TimeDcode
```
or
```cmd
py TimeDcode
```

## Usage Instructions

### Single Conversion Mode

1. **Enter Timestamp**: Type or paste your timestamp value into the "Input Timestamp" field
   - Hex values can include `0x` prefix, spaces, or colons (they will be automatically cleaned)
   - Examples: `0x65000000`, `1696118400`, `65000000`

2. **Select Format**: Choose the timestamp format from the "Source Format" dropdown menu

3. **Select Target Timezone** (Optional): Choose a timezone from the "Optional Target Timezone" dropdown
   - Default is "America/Los_Angeles"
   - You can type to search for timezones

4. **Click "CONVERT (Single)"**: The application will display:
   - **UTC Time**: The timestamp converted to UTC
   - **Local Time**: The timestamp converted to your system's local timezone
   - **Target Time**: The timestamp converted to your selected target timezone

5. **Copy Results**: Click and drag to select any of the time values, then copy (Ctrl+C / Cmd+C) and paste as needed

### Guess All Formats Mode

1. **Enter Timestamp**: Type or paste your timestamp value (format unknown)

2. **Click "GUESS / CHECK ALL"**: The application will:
   - Test the input against all 7 supported formats
   - Filter results to show only dates between 1970-2040
   - Display all valid matches in the scrollable results area

3. **Review Results**: Each match shows:
   - The format that produced the match
   - The decoded date and time in UTC

### Copying Time Values

All decoded times (UTC, Local, and Target) are displayed in readonly entry fields that allow text selection:
- Click and drag to select the time value
- Use Ctrl+C (Windows/Linux) or Cmd+C (macOS) to copy
- Paste into any application

## Example Usage

### Example 1: Unix Hex Timestamp
**Input**: `0x65000000`  
**Format**: Unix Hex 32-bit Big Endian  
**Result**: 
- UTC Time: 2023-10-01 00:00:00.000000
- Local Time: 2023-09-30 17:00:00.000000 PDT
- Target Time: 2023-09-30 17:00:00.000000 PDT

### Example 2: Unix Decimal Timestamp
**Input**: `1696118400`  
**Format**: Unix Seconds (Decimal)  
**Result**: 
- UTC Time: 2023-10-01 00:00:00.000000
- Local Time: 2023-09-30 17:00:00.000000 PDT

### Example 3: Guess Mode
**Input**: `65000000`  
**Action**: Click "GUESS / CHECK ALL"  
**Result**: Shows all valid interpretations of this value across different formats within the 1970-2040 date range

## Notes

- The application performs sanity checks to prevent dates outside reasonable bounds
- Guess mode filters results to dates between 1970-2040 to reduce false positives
- All timezone conversions use the IANA timezone database
- The application window is resizable for better usability
