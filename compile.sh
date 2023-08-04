#!/bin/bash

if [ ! -d ".venv" ]; then
    python -m venv .venv
    source .venv/bin/activate
    python.exe -m pip install --upgrade pip
    pip install -r requirements.txt
    deactivate
fi

source .venv/bin/activate
pyinstaller --onefile --name SimVex SimVex.py --distpath ./ --noconsole --clean
deactivate

rm SimVex.spec
rm -rf build