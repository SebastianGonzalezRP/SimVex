#!/bin/bash



# Activate the virtual environment
source .venv/Scripts/activate

pyinstaller --onefile --name SimVex SimVex.py --distpath ./ --noconsole

deactivate