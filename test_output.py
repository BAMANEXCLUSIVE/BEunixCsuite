#!/usr/bin/env python3
import os

# Determine the local OUTPUT directory (relative to current working directory)
OUTPUT_DIR = os.path.join(os.getcwd(), "OUTPUT")
print("OUTPUT_DIR is:", OUTPUT_DIR)

# Ensure the directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Define the test file path
test_file = os.path.join(OUTPUT_DIR, "test_output.txt")

# Write content to the test file and flush immediately
with open(test_file, "w") as f:
    f.write("This is a test.\n")
    f.flush()
    os.fsync(f.fileno())

print("Test file written to:", test_file)
