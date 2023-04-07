#!/bin/bash

# Check if a virtual environment exists
if [ ! -d "venv" ]
then
    # Create a virtual environment
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install the required packages
pip install -r requirements.txt

# Open website and run the app
xdg-open http://127.0.0.1:5000/website && python3 app.py