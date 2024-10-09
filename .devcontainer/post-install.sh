#!/bin/bash

# Ensure that Poetry environment is activated
echo "Activating Poetry environment..."
source $(poetry env info --path)/bin/activate

# Install any additional Python packages if needed
echo "Installing additional Python packages..."
poetry install
