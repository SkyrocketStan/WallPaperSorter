# Wallpaper Sorter

A Python script to efficiently sort desktop wallpapers by resolution and aspect ratio, designed to run in a Podman container for portability and isolation. The project includes a Bash wrapper for simplified execution, supporting dry-run simulations and modern development practices.

## Features

- **Fast and Efficient**: Uses parallel processing with Python's `ThreadPoolExecutor` to sort large collections of JPEG files quickly.
- **Containerized**: Runs in a lightweight Podman container based on `python:3.11-slim`.
- **User-Friendly**: Bash script (`sort-wallpapers.sh`) simplifies execution with intuitive `--input`, `--output`, and `--dry-run` options.
- **Modern Standards**: Adheres to PEP 8, Clean Code principles, and includes type hints for maintainability.
- **Robust**: Handles corrupt files, invalid JPEGs, and permission issues with detailed logging.
- **Dry Run Support**: Simulate sorting operations without modifying files using the `--dry-run` flag.

## Prerequisites

- **Podman**: Required to build and run the container. Install with:

  ```bash
  sudo dnf install podman  # On Fedora
  sudo apt install podman  # On Ubuntu
  ```

- **Bash**: For running the `sort-wallpapers.sh` script (available on most Linux systems).
- **JPEG Files**: The script processes `.jpg` and `.jpeg` files (case-insensitive).

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/wallpaper-sorter.git
   cd wallpaper-sorter
   ```

2. Ensure the Bash script is executable:

   ```bash
   chmod +x sort-wallpapers.sh
   ```

## Usage

The `sort-wallpapers.sh` script simplifies running the sorter. It builds the Podman container if needed and processes JPEG files from an input directory, sorting them into an output directory by aspect ratio (e.g., `16x9`, `16x10`, `4x3`) and resolution (e.g., `1920x1080`).

### Basic Commands

- **Dry Run** (simulate sorting):

  ```bash
  ./sort-wallpapers.sh --input /path/to/unsorted --output /path/to/sorted --dry-run
  ```

- **Actual Run** (sort files):

  ```bash
  ./sort-wallpapers.sh --input /path/to/unsorted --output /path/to/sorted
  ```

### Example

To sort wallpapers from `/home/stan/Pictures/unsort-wp` to `/home/stan/Pictures/wallpapers`:

```bash
./sort-wallpapers.sh --input /home/stan/Pictures/unsort-wp --output /home/stan/Pictures/wallpapers
```

This creates a structure like:

```plaintext
/home/stan/Pictures/wallpapers/
├── 16x9/
│   ├── 1920x1080/
│   │   ├── image1.jpg
├── 4x3/
│   ├── 1024x768/
│   │   ├── image2.jpg
├── broke_and_unsort/
│   ├── non_jpeg.png
```

### Options

- `--input <dir>`: Directory containing unsorted wallpapers (required).
- `--output <dir>`: Directory for sorted wallpapers (required).
- `--dry-run`: Simulate operations without moving or deleting files (optional).

## How It Works

1. **Python Script (`wallpapers.py`)**:
   - Reads JPEG headers to determine resolution.
   - Classifies images by aspect ratio (`16x9`, `16x10`, `4x3`, or `broke_and_unsort` for unknown/invalid files).
   - Moves files to the output directory in parallel for speed.
   - Cleans up empty directories in the input path.

2. **Bash Wrapper (`sort-wallpapers.sh`)**:
   - Builds the Podman container if it doesn’t exist.
   - Maps local directories to container paths (`/data/wallpapers` for input, `/data/sorted` for output).
   - Passes arguments to the Python script.

3. **Podman Container (`Dockerfile`)**:
   - Uses a lightweight `python:3.11-slim` base image.
   - Installs minimal dependencies (e.g., Pillow for potential future use).
   - Runs the Python script with default paths for simplicity.

## Output

- **Logs**: Detailed logs show each file’s movement or errors, e.g.:

  ```plaintext
  2025-05-01 12:00:00,000 - INFO - Starting wallpaper sorting: input=/data/wallpapers, output=/data/sorted, dry_run=False
  2025-05-01 12:00:00,100 - INFO - Moved /data/wallpapers/image1.jpg to /data/sorted/16x9/1920x1080
  ```

- **Directory Structure**: Organized by aspect ratio and resolution, with non-JPEG or invalid files in `broke_and_unsort`.

## Troubleshooting

- **Podman Not Found**: Install Podman (see Prerequisites).
- **Permission Denied**: Ensure read/write permissions:

  ```bash
  chmod -R u+rw /path/to/unsorted /path/to/sorted
  ```

- **No Files Processed**: Verify the input directory contains `.jpg` or `.jpeg` files.
- **Build Fails**: Ensure `wallpapers.py` and `Dockerfile` are in the same directory as `sort-wallpapers.sh`.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

Please ensure code follows PEP 8 and includes tests where applicable.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

For issues or feature requests, open an issue on GitHub or contact [your-username]@example.com.
