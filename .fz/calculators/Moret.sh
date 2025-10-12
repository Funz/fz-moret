#!/bin/bash

# Moret calculator script for fz
# This script runs MORET calculations

# Check if we received a directory or files as input
if [ -d "$1" ]; then
  # If directory, cd into it
  cd "$1"
  M5FILE=`ls *.m5 2>/dev/null | head -n 1`
  shift
elif [ $# -gt 0 ]; then
  # If files are provided, find the .m5 file
  M5FILE=""
  for f in "$@"; do
    if [[ "$f" =~ \.m5$ ]]; then
      M5FILE="$f"
      break
    fi
  done
  
  if [ -z "$M5FILE" ]; then
    echo "No .m5 file found in input files. Exiting."
    exit 1
  fi
  shift $#
else
  echo "Usage: $0 <input.m5 or input_directory>"
  exit 2
fi

# Check if M5FILE was found
if [ -z "$M5FILE" ]; then
  echo "No .m5 file found. Exiting."
  exit 1
fi

# Check if the file contains MORET markers
if ! grep -q "MORET" "$M5FILE"; then
  echo "Input file does not appear to be a MORET file (missing MORET markers)"
  exit 3
fi

# Check if MORET is installed
if [ ! -f "/opt/MORET/scripts/moret.py" ]; then
  echo "MORET is not installed at /opt/MORET/scripts/moret.py"
  echo "Please install MORET or update the path in this script"
  exit 4
fi

# Run MORET
/opt/MORET/scripts/moret.py "$M5FILE"

# Check if the calculation produced output
LISTING_FILE="${M5FILE%.m5}.listing"
if [ ! -f "$LISTING_FILE" ]; then
  echo "MORET calculation did not produce expected output file: $LISTING_FILE"
  exit 5
fi

echo "MORET calculation completed successfully"
exit 0
