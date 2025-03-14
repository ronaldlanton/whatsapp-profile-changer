# WhatsApp Profile Changer

An automated tool to change your WhatsApp Web profile picture at regular intervals.

## Features

- **Sequence Mode**: Cycle through a series of profile pictures in order
- **Clock Mode**: Display a real-time clock as your profile picture (showing India Standard Time)
- **Customizable Duration**: Set how long each profile picture should be displayed
- **Automated Process**: Once set up, the tool handles the entire profile changing process
- **Configuration File**: Easily configure settings through a config file
- **Command Line Interface**: Override settings via command line arguments

## Requirements

- Python 3.6+
- Chrome browser
- Selenium WebDriver

## Installation

### From Source

1. Clone this repository:
   ```
   git clone https://github.com/ronaldlanton/whatsapp-profile-changer.git
   cd whatsapp-profile-changer
   ```

2. Install the package:
   ```
   pip install -e .
   ```

3. Download ChromeDriver that matches your Chrome version from [here](https://sites.google.com/chromium.org/driver/) and place it in your PATH.

### Using pip

```
pip install whatsapp-profile-changer
```

## Usage

### Basic Usage

1. Place your profile pictures in a folder named `pics` (numbered sequentially like 1.png, 2.png, etc.)

2. Run the tool:
   ```
   whatsapp-profile-changer
   ```

3. Scan the QR code that appears to log in to WhatsApp Web

4. The program will automatically change your profile picture at the specified interval

### Command Line Options

```
usage: whatsapp-profile-changer [-h] [-c CONFIG] [-m {sequence,clock}] [-d DURATION] [-p PICS_FOLDER]

WhatsApp Profile Changer - Change your WhatsApp Web profile picture automatically.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to configuration file
  -m {sequence,clock}, --mode {sequence,clock}
                        Mode: "sequence" or "clock"
  -d DURATION, --duration DURATION
                        Duration in seconds to display each picture
  -p PICS_FOLDER, --pics-folder PICS_FOLDER
                        Folder containing profile pictures
```

### Configuration File

You can customize the behavior by creating a `config.ini` file:

```ini
[Settings]
# Folder containing profile pictures
pics_folder = pics

# Duration in seconds to display each picture
duration = 5

# Mode: "sequence" or "clock"
mode = sequence

# Timeout in seconds to wait for login
timeout = 300

# Folder for temporary clock images
temp_folder = temp_clock
```

## Project Structure

```
whatsapp_profile_changer/
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
├── config.ini
├── run.py
├── whatsapp_profile_changer/
│   ├── __init__.py
│   ├── browser.py
│   ├── image_handler.py
│   ├── config.py
│   └── profile_changer.py
└── pics/
    ├── 1.png
    ├── 2.png
    └── 3.png
```

## How It Works

The script uses Selenium to automate the WhatsApp Web interface:

1. Opens WhatsApp Web and waits for you to scan the QR code
2. Navigates to the profile settings
3. Uploads a new profile picture from the pics folder
4. Waits for the specified duration
5. Repeats the process with the next picture

In clock mode, it generates a new clock image showing the current time before each update.

## Troubleshooting

- If the script fails to find elements, it may be due to WhatsApp Web UI changes. Check the console for error messages.
- Make sure your Chrome browser is up to date.
- Ensure your internet connection is stable.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational purposes only. Use it responsibly and at your own risk. The developers are not responsible for any account restrictions that may result from automated usage of WhatsApp Web.