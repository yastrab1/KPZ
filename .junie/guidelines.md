# Developer Guidelines

## Project Overview
This project is a utility suite that provides various tools for media processing and manipulation. It consists of a backend that compiles Python scripts into standalone executables and a frontend that downloads and manages these executables.

## Tech Stack
- **Python**: The primary programming language used throughout the project
- **OpenCV (cv2)**: Used for image processing
- **NumPy**: Used for numerical operations in image processing
- **Segno**: Used for QR code generation
- **yt-dlp**: Used for YouTube video downloading
- **PyInstaller**: Used to compile Python scripts into standalone executables
- **Requests**: Used in the frontend to download executables from the backend

## Project Structure
- **back/**: Backend code
  - **pkgs/**: Python packages that are compiled into executables
    - **img.py**: Image processing utility (in development)
    - **qr.py**: QR code generation utility
    - **yt.py**: YouTube video download utility
  - **build/**: Build artifacts generated during compilation
  - **dist/**: Distribution files (compiled executables)
  - **compile.py**: Script that compiles Python packages into executables
- **front/**: Frontend code
  - **bin/**: Directory for downloaded executables
  - **manager.py**: Script that downloads and manages executables
- **create/**: Python virtual environment for content creation
- **.venv/**: Main Python virtual environment

## Running Scripts

### Backend
1. To compile Python packages into executables:
   ```
   cd back
   python3 compile.py
   ```
   This will compile all Python scripts in the `pkgs` directory into standalone executables and place them in the `dist` directory.

### Frontend
1. To download and install executables:
   ```
   cd front
   python3 manager.py
   ```
   This will download all executables from the backend server and place them in the `bin` directory, which is added to the system PATH.

## Executing Utilities
Once the utilities are installed, they can be executed from the command line:

- **QR Code Generation**:
  ```
  qr -d "Data to encode" -o output.png
  ```

- **YouTube Download**:
  ```
  yt [yt-dlp arguments]
  ```

## Best Practices
1. **Package Development**:
   - Place new utility scripts in the `back/pkgs` directory
   - Use `argparse` for command-line argument parsing
   - Keep scripts focused on a single functionality
   - Document the script's usage with comments

2. **Compilation**:
   - Run `compile.py` after making changes to any script in `pkgs`
   - Ensure all dependencies are properly imported
   - Test the compiled executables before distribution

3. **Frontend Development**:
   - Update the frontend manager if new executables need to be downloaded
   - Ensure the server is running before using the manager
   - Test the downloaded executables to ensure they work correctly

4. **General**:
   - Follow Python PEP 8 style guidelines
   - Document code with comments and docstrings
   - Keep dependencies minimal and explicit
   - Use virtual environments for development
