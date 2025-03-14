# WhatsApp Profile Changer

An automated tool to change your WhatsApp Web profile picture at regular intervals.

## Features

- **Sequence Mode**: Cycle through a series of profile pictures in order
- **Clock Mode**: Display a real-time clock as your profile picture (showing India Standard Time)
- **Customizable Duration**: Set how long each profile picture should be displayed
- **Automated Process**: Once set up, the tool handles the entire profile changing process

## Requirements

- Python 3.6+
- Chrome browser
- Selenium WebDriver
- PIL (Python Imaging Library)
- pytz

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/whatsapp-profile-changer.git
   cd whatsapp-profile-changer
   ```

2. Install the required packages:
   ```
   pip install selenium pillow pytz
   ```

3. Download ChromeDriver that matches your Chrome version from [here](https://sites.google.com/chromium.org/driver/) and place it in your PATH or in the project directory.

## Usage

1. Place your profile pictures in the `pics` folder (numbered sequentially like 1.png, 2.png, etc.)

2. Run the script:
   ```
   python Whatsapp_profilechanger.py
   ```

3. Scan the QR code that appears to log in to WhatsApp Web

4. The program will automatically change your profile picture at the specified interval

## Configuration

You can modify the following parameters in the script:

- `pics_folder`: Directory containing profile pictures (default: "pics")
- `duration`: Time in seconds to display each picture (default: 5)
- `mode`: Either "sequence" (cycle through pictures) or "clock" (show a real-time clock)

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