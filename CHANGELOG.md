# Changelog

All notable changes to the WallPaperSorter project will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Dynamic aspect ratio detection, sorting into `16x9`, `4x3`, `16x10` for FHD/2K/4K resolutions, with non-standard or invalid files in `unsort`.
- Content-based duplicate detection using MD5 hashes, appending `_1`, `_2` suffixes, with `hashes.json` in the output directory for sorted files.
- File renaming using EXIF `DateTimeOriginal` (`YYYYMMDD_HHMMSS.jpg`), creation date, or original filename if unavailable.
- Summary statistics (total files, processed, erroneous, duplicates renamed, execution time).
- Global Bash script installation via `install.sh` for `/usr/local/bin/sort-wallpapers`.
- Pylint CI workflow for code quality checks.

### Changed
- Replaced `broke_and_unsort` with `unsort` for invalid/non-standard files.
- Removed hard-coded aspect ratio list for dynamic detection.

## [2.1.0] - 2025-05-01
### Added
- Podman containerization with `Dockerfile` and `sort-wallpapers.sh` Bash wrapper.
- PNG file support alongside JPEG (`.jpg`, `.jpeg`).
- Progress bar using `tqdm` for processing large directories.
- Error summary for failed file operations.
- Command-line interface with `--input`, `--output`, `--dry-run` flags.
- Parallel processing with `ThreadPoolExecutor` for performance.

### Changed
- Refactored `wallpapers.py` for modern Python (3.11), PEP 8 compliance, and type hints.
- Improved logging and error handling.
- Updated README with setup, usage, and Podman instructions.

## [2.0.0] - 2017-09-18
### Added
- Command-line arguments for source (`wallpapers`) and destination (`source.sorted`) directories.
- Support for `.jpeg` alongside `.jpg` (case-insensitive).
- Automatic deletion of empty source directories.
- Sorting into `<destination_dir>/<aspect>/<resolution>` with `broke_and_unsort` for unrecognized files.

### Changed
- Enhanced file type checking and directory handling over `v1.0.0`.
- Updated README with new usage instructions.

### Fixed
- Improved handling of JPEG headers for resolution detection.

## [1.0.0] - 2016-02-29
### Added
- Initial Python script (`wallpapers.py`) for sorting JPEG (`.jpg`) files.
- Sorting into `./sorted/<aspect>/<resolution>` folders, with `unsort` for unrecognized files.
- Hard-coded aspect ratios (`16x9`, `4x3`, `16x10`) and resolutions.
- Basic README with usage instructions.

### Notes
- Designed for Python 3.5.0 on Windows (64-bit).