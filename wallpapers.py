import argparse
import logging
import os
import shutil
import struct
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_INPUT_DIR = Path("/data/wallpapers")
DEFAULT_OUTPUT_DIR = Path("/data/sorted")
DEFAULT_BROKE_DIR = Path("broke_and_unsort")
ASPECT_RATIOS = {
    "16x9": [
        "640x360", "720x405", "854x480", "960x540", "1024x576", "1280x720",
        "1366x768", "1600x900", "1920x1080", "2048x1152", "2560x1440",
        "2880x1620", "3200x1800", "3840x2160", "4096x2304", "5120x2880",
        "7680x4320", "15360x8640"
    ],
    "16x10": ["1280x800", "1440x900", "1680x1050", "1920x1200", "2560x1600"],
    "4x3": [
        "640x480", "800x600", "1024x768", "1152x864", "1280x960", "1400x1050",
        "1600x1200", "2048x1536", "3200x2400", "4000x3000", "6400x4800"
    ]
}

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Sort wallpaper images by resolution and aspect ratio.")
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help="Directory containing unsorted wallpapers"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for sorted wallpapers"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate operations without modifying files"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=os.cpu_count() or 4,
        help="Number of worker threads for parallel processing"
    )
    return parser.parse_args()

def get_image_size(file_path: Path) -> str:
    """Determine the image size by reading the JPEG header."""
    try:
        with file_path.open("rb") as file_handle:
            file_handle.seek(0)
            size = 2
            ftype = 0
            while not 0xc0 <= ftype <= 0xcf:
                file_handle.seek(size, 1)
                byte = file_handle.read(1)
                while ord(byte) == 0xff:
                    byte = file_handle.read(1)
                ftype = ord(byte)
                size = struct.unpack(">H", file_handle.read(2))[0] - 2
            file_handle.seek(1, 1)
            height, width = struct.unpack(">HH", file_handle.read(4))
            return f"{width}x{height}"
    except Exception as e:
        logger.warning(f"Failed to read size of {file_path}: {e}")
        return "Unknown"

def get_aspect_ratio(size: str) -> str:
    """Determine the aspect ratio based on image size."""
    for ratio, sizes in ASPECT_RATIOS.items():
        if size in sizes:
            return ratio
    return DEFAULT_BROKE_DIR.name

def is_jpeg_file(file_path: Path) -> bool:
    """Check if the file is a valid JPEG."""
    try:
        with file_path.open("rb") as f:
            return f.read(2) == b"\xFF\xD8"  # JPEG start of image marker
    except (FileNotFoundError, IOError) as e:
        logger.warning(f"Error checking file type for {file_path}: {e}")
        return False

def process_file(file_path: Path, output_dir: Path, dry_run: bool) -> None:
    """Process a single file by sorting it into the appropriate directory."""
    if not is_jpeg_file(file_path):
        target_dir = output_dir / DEFAULT_BROKE_DIR
    else:
        image_size = get_image_size(file_path)
        aspect = get_aspect_ratio(image_size)
        target_dir = output_dir / aspect / image_size

    if dry_run:
        logger.info(f"[Dry Run] Would move {file_path} to {target_dir}")
        return

    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(file_path), str(target_dir))
        logger.info(f"Moved {file_path} to {target_dir}")
    except (shutil.Error, OSError) as e:
        logger.error(f"Failed to move {file_path} to {target_dir}: {e}")

def process_directory(directory: Path, output_dir: Path, dry_run: bool, workers: int) -> None:
    """Process all JPEG files in the directory using parallel processing."""
    files = [
        directory / f for f in directory.iterdir()
        if f.is_file() and f.suffix.lower() in (".jpg", ".jpeg")
    ]
    if not files:
        logger.debug(f"No JPEG files found in {directory}")
        return

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(process_file, file, output_dir, dry_run)
            for file in files
        ]
        for future in futures:
            future.result()  # Wait for completion and handle exceptions

def clean_empty_directories(directory: Path, dry_run: bool) -> None:
    """Remove empty directories recursively."""
    for dir_path in sorted(directory.rglob("*"), reverse=True):
        if dir_path.is_dir() and not any(dir_path.iterdir()):
            if dry_run:
                logger.info(f"[Dry Run] Would delete empty directory {dir_path}")
            else:
                try:
                    dir_path.rmdir()
                    logger.info(f"Deleted empty directory {dir_path}")
                except OSError as e:
                    logger.warning(f"Failed to delete {dir_path}: {e}")

def main() -> None:
    """Main function to orchestrate wallpaper sorting."""
    args = parse_arguments()
    input_dir = args.input.resolve()
    output_dir = args.output.resolve()
    dry_run = args.dry_run
    workers = args.workers

    if not input_dir.exists():
        logger.error(f"Input directory {input_dir} does not exist")
        return

    logger.info(f"Starting wallpaper sorting: input={input_dir}, output={output_dir}, dry_run={dry_run}")

    # Process all directories recursively
    for directory in input_dir.rglob("*"):
        if directory.is_dir():
            process_directory(directory, output_dir, dry_run, workers)

    # Clean up empty directories
    clean_empty_directories(input_dir, dry_run)

if __name__ == "__main__":
    main()
