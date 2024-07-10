#!/bin/bash

# Directory to store past releases
PAST_RELEASES_DIR="PAST_RELEASES"

# Create the directory if it does not exist
mkdir -p "$PAST_RELEASES_DIR"

# Find all .app files in the root directory, sort them by modification time, and skip the newest
apps_to_move=$(ls -t *.app | tail -n +2)

# Check if there is more than one .app file
if [ $(echo "$apps_to_move" | wc -l) -gt 0 ]; then
    # Move all .app files except the newest to the PAST_RELEASES directory
    echo "Moving older .app files to $PAST_RELEASES_DIR..."
    for app in $apps_to_move; do
        mv "$app" "$PAST_RELEASES_DIR/"
    done
else
    echo "No old .app files to move."
fi