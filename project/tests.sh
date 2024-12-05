#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Defining paths
PIPELINE_SCRIPT="./project/pipeline.py"
DATA_DIR="./data"
OUTPUT_DB="$DATA_DIR/project_data.db"

# Step 1: Running the data pipeline
echo "Running the data pipeline..."
python3 $PIPELINE_SCRIPT

# Step 2: Validating the output
echo "Validating the output..."

# Checking if the output database file exists
if [ -f "$OUTPUT_DB" ]; then
    echo "SUCCESS: Output database file exists at $OUTPUT_DB"
else
    echo "ERROR: Output database file does not exist."
    exit 1
fi

# Checking the database contents using sqlite3
echo "Checking database contents..."
TABLES=$(sqlite3 $OUTPUT_DB ".tables")
if [[ "$TABLES" == *"ev_data"* && "$TABLES" == *"emissions_data"* ]]; then
    echo "SUCCESS: Expected tables 'ev_data' and 'emissions_data' found."
else
    echo "ERROR: Expected tables not found in the database."
    exit 1
fi

echo "All tests passed successfully!"
