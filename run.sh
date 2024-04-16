#!/bin/sh

set -e

pip3 install -r requirements.txt
source .env
python3 main.py
