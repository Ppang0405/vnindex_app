# VN-Index Status Bar App

A macOS status bar application that displays real-time VN-Index data.

## Features

- Real-time VN-Index data in your macOS menu bar
- Support for multiple indices: VN-Index, VN30, HNX-Index
- Auto-updates every 60 seconds
- Manual refresh option

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd vnindex_app
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the application directly:
   ```
   python main.py
   ```

## Building the App

To build a standalone macOS application:

1. Ensure you have py2app installed:
   ```
   pip install py2app
   ```

2. Build the application:
   ```
   python setup.py py2app
   ```

3. The built application will be available in the `dist` directory.

## Usage

- The app displays the current VN-Index value in the status bar
- Click on the status bar icon to see the menu
- Select different indices to display (VN-Index, VN30, HNX-Index)
- Use the "Refresh" option to manually update the data

## Requirements

- macOS
- Python 3.6+
- Internet connection to fetch index data

## Data Source

This application uses the `vnstock` Python package to retrieve real-time VN-Index data.
