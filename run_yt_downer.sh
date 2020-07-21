#!/bin/sh
. .env/bin/activate
alias python=.env/bin/python3.8
python -V
python -m pip -V
python run.py "$@"