# Work Hours Calculator

## Overview
The **Work Hours Calculator** is a Python application designed to help you track and calculate work hours efficiently. By providing clock-in and clock-out times, the app calculates the total hours worked and stores this data for future reference. It can also display the work hours in a table for easy review.

## Features
- **Clock-in and Clock-out**: Record start and end times for work.
- **Data Storage**: Automatically stores work hours for later use.
- **Data Display**: View stored work hours in a tabular format.
- **User-Friendly Interface**: Built using Python's Tkinter library for an intuitive graphical user interface.

## Requirements  
- Python >= 3.8

## Installation  [![Release](https://img.shields.io/github/v/release/mdoganer/work-hours-calculator)](https://github.com/mdoganer/work-hours-calculator/releases/tag/v0.1.0)
1. Clone the repository:
   ```bash
   git clone https://github.com/mdoganer/work-hours-calculator.git
   ```
2. Navigate to the project directory:
   ```bash
   cd work-hours-calculator
   ```
   
## Usage
1. Run the application:
   ```bash
   python app.py
   ```
2. Use the graphical interface to clock in, clock out, and view your work hours.

## Build Your App Executable
To create an executable version of the application with proper language support, use the included build script:

1. Install `pyinstaller` if you haven't already:
   ```bash
   pip install pyinstaller
   ```

2. Run the build script:
   ```bash
   python build.py
   ```
   
   This script will:
   - Generate a PyInstaller spec file with proper language file inclusion
   - Build the application with all necessary resources
   - Place the final executable in the `dist` directory

3. The executable will be available in the `dist` directory.

> **Note**: The build script ensures that language files are properly included in the executable, which is necessary for the application to function correctly.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push the branch:
   ```bash
   git commit -m "Description of changes"
   git push origin feature-name
   ```
4. Open a pull request on GitHub.

## License
This project is open-source and available under the [MIT License](LICENSE).

## Contact
For any questions or feedback, feel free to open an issue or contact [mdoganer](https://github.com/mdoganer).
