#!/bin/bash
# Quick script to run view generation
if [ -d "venv" ]; then
    source venv/bin/activate
fi
python3 run_simulation.py "$@"
