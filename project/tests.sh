#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define paths
PIPELINE_SCRIPT="./project/pipeline.py"
DATA_DIR="./project/data"
OUTPUT_DB="$DATA_DIR/project_data.db"

# Step 1: Run the data pipeline
echo "Running the data pipeline..."
python3 $PIPELINE_SCRIPT

# Step 2: Validate the data directory
echo "Validating the data directory..."
if [ -d "$DATA_DIR" ]; then
    echo "SUCCESS: Data directory exists at $DATA_DIR"
else
    echo "ERROR: Data directory does not exist."
    exit 1
fi

# Step 3: Validate the database file
echo "Validating the database file..."
if [ -f "$OUTPUT_DB" ]; then
    echo "SUCCESS: Output database file exists at $OUTPUT_DB"
else
    echo "ERROR: Output database file does not exist."
    echo "Attempted path: $OUTPUT_DB"
    ls -R "$DATA_DIR"  # List contents of the data directory for debugging
    exit 1
fi

# Additional checks
echo "Checking database contents..."
TABLES=$(sqlite3 $OUTPUT_DB ".tables")
if [[ "$TABLES" == *"ev_data"* && "$TABLES" == *"emissions_data"* ]]; then
    echo "SUCCESS: Expected tables 'ev_data' and 'emissions_data' found."
else
    echo "ERROR: Expected tables not found in the database."
    exit 1
fi

echo "All tests passed successfully!"
