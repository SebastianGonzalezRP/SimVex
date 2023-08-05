#!/bin/bash

if [ ! -d ".venv" ]; then
    python -m venv .venv
fi  

source .venv/Scripts/activate
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
pyinstaller --onefile --name SimVex SimVex.py --distpath ./ --noconsole --clean
deactivate

rm SimVex.spec
rm -rf build