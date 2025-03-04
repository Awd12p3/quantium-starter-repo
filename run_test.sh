#!/usr/bin/env bash

# Check for the correct virtual environment activation script
if [ -f "venv/Scripts/activate" ]; then
  source venv/Scripts/activate
elif [ -f "venv/bin/activate" ]; then
  source venv/bin/activate
else
  echo "Virtual environment activation script not found!"
  exit 1
fi

# Run the test suite with pytest
pytest test_app.py
result=$?

# Check the exit code and print an appropriate message
if [ $result -eq 0 ]; then
    echo "All tests passed!"
    exit 0
else
    echo "Some tests failed."
    exit 1
fi
