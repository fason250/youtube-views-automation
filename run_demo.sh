#!/bin/bash
# Quick script to run demo
if [ -d "venv" ]; then
    source venv/bin/activate
fi
python3 demo_dry_run.py
