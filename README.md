# Flask Data Capture (Educational Project)

⚠️ DISCLAIMER: This project was created for **educational and didactic purposes only**.  
It is **NOT intended for malicious use**.

## Installation
1. Install Python (>=3.12)
2. Install required libraries:
   `pip install Flask requests`
3. Run the server:
   `python ctrap.py --server`

## About
This script allows you to:
- Run a Flask server that captures client data (IP, headers, cookies, approximate location).
- Inject a `<link>` tag into any `.html` file, making it usable for **social engineering demonstrations**.  
  When someone opens the modified HTML file, their data is captured and logged.

## Features
- `-h, --help`   → Show command usage.
- `-c, --config` → Save host and port configuration.
- `-s, --server` → Run the server with saved configuration.
- `-sf, --set-file FILE URL` → Insert a `<link>` tag into a `.html` file.
- `-l, --list`   → List captured data.
- `-r, --reset`  → Clear all captured data.

## Disclaimer
This script is designed **only for training, study, and demonstration of social engineering concepts**.  
Do not use it for real phishing campaigns or malicious activity.
