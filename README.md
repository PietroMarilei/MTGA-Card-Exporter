# MTGA Card Exporter

[Download MTGA Card Exporter Executable](link-to-your-exe-file)

## Description
MTGA Card Exporter is a Python-based application designed to extract card information from Magic: The Gathering Arena (MTGA) log files and convert card IDs to their corresponding names using the AllPrintings.json file from MTGJSON.

## Disclaimer
This application is not affiliated with, endorsed, sponsored, or specifically approved by Wizards of the Coast LLC or Hasbro Inc. This application may use trademarks and/or copyrights owned by Wizards of the Coast LLC and Hasbro Inc., which are used under Wizards' Fan Content Policy. This application is not produced by, endorsed by, supported by, or affiliated with Wizards of the Coast LLC or Hasbro Inc.

All card names, artwork, and related content are copyright © of Wizards of the Coast LLC, a subsidiary of Hasbro, Inc. This application does not reproduce any copyrighted material and is intended for personal, non-commercial use only.

## Features
- Extract card IDs and quantities from MTGA log files
- Convert card IDs to card names using AllPrintings.json
- Export results to CSV files
- User-friendly graphical interface

## Requirements and Installation
- Python 3.x
- tkinter (usually comes pre-installed with Python)
- Internet connection to download AllPrintings.json (if not already available)

To install:
1. Clone this repository or download the source code.
2. Ensure you have Python 3.x installed on your system.
3. No additional dependencies are required.

## Usage
1. Run the script: `python mtga_collection_exporter.py`
2. Use the GUI to select your MTGA log file (usually named "UTC_Log-*.log").
3. Select the AllPrintings.json file (download from MTGJSON if you don't have it).
4. Click "Extract Card IDs" to get a CSV of card IDs and quantities.
5. Click "Convert to Card Names" to get a CSV with card names included.

## File Locations
- MTGA Log Files: 
  - Windows (Steam version): `C:\Program Files (x86)\Steam\steamapps\common\MTGA\MTGA_Data\Logs\Logs`
    The file is named `UTC_Log - [date].log`
  - Windows (Standard version): `%appdata%/../LocalLow/Wizards Of The Coast/MTGA`
  - macOS: `~/Library/Logs/Wizards Of The Coast/MTGA`
- AllPrintings.json: Download from [MTGJSON](https://mtgjson.com/downloads/all-files/)

## Output and Troubleshooting
The application generates two types of CSV files:
1. `deck_card_ids_[timestamp].csv`: Contains card IDs and quantities
2. `deck_card_names_[timestamp].csv`: Contains card IDs, names, and quantities

If card names are not found, ensure you're using the latest version of AllPrintings.json. Check the console output for additional debugging information.

## Contributing
Contributions, issues, and feature requests are welcome. Feel free to check [issues page](link-to-your-issues-page) if you want to contribute.

## License
This project is released under the [MIT License](https://choosealicense.com/licenses/mit/).

## Acknowledgments
- MTGJSON for providing comprehensive MTG card data
- The MTGA community for insights into log file structures

This application is intended for educational and personal use only. Users are responsible for ensuring their use of this application complies with Wizards of the Coast's Fan Content Policy and all applicable laws and regulations.
