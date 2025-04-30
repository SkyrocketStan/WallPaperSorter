#!/bin/bash

# Wallpaper sorting script to run the Python sorter in a Podman container

# Configuration
IMAGE_NAME="wallpaper-sorter"
CONTAINER_INPUT_DIR="/data/wallpapers"
CONTAINER_OUTPUT_DIR="/data/sorted"

# Usage function
usage() {
    echo "Usage: $0 --input <input_dir> --output <output_dir> [--dry-run]"
    echo "  --input   Directory containing unsorted wallpapers"
    echo "  --output  Directory for sorted wallpapers"
    echo "  --dry-run Simulate sorting without modifying files"
    exit 1
}

# Parse arguments
INPUT_DIR=""
OUTPUT_DIR=""
DRY_RUN=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --input)
            INPUT_DIR="$2"
            shift 2
            ;;
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN="--dry-run"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# Validate arguments
if [[ -z "$INPUT_DIR" || -z "$OUTPUT_DIR" ]]; then
    echo "Error: Both --input and --output are required"
    usage
fi

# Check if input directory exists
if [[ ! -d "$INPUT_DIR" ]]; then
    echo "Error: Input directory '$INPUT_DIR' does not exist"
    exit 1
fi

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR" || {
    echo "Error: Failed to create output directory '$OUTPUT_DIR'"
    exit 1
}

# Check if Podman is installed
if ! command -v podman &> /dev/null; then
    echo "Error: Podman is not installed. Please install Podman and try again."
    exit 1
fi

# Build the container image if it doesn't exist
if ! podman image exists "$IMAGE_NAME"; then
    echo "Building Podman container image '$IMAGE_NAME'..."
    podman build -t "$IMAGE_NAME" . || {
        echo "Error: Failed to build container image"
        exit 1
    }
fi

# Run the container
echo "Running wallpaper sorter: input=$INPUT_DIR, output=$OUTPUT_DIR, dry_run=$([[ -n $DRY_RUN ]] && echo 'true' || echo 'false')"
podman run --rm \
    -v "$(realpath "$INPUT_DIR"):$CONTAINER_INPUT_DIR" \
    -v "$(realpath "$OUTPUT_DIR"):$CONTAINER_OUTPUT_DIR" \
    "$IMAGE_NAME" \
    --input "$CONTAINER_INPUT_DIR" \
    --output "$CONTAINER_OUTPUT_DIR" \
    $DRY_RUN

# Check exit status
if [[ $? -eq 0 ]]; then
    echo "Wallpaper sorting completed successfully"
else
    echo "Error: Wallpaper sorting failed"
    exit 1
fi