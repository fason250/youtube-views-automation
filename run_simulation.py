#!/usr/bin/env python3
"""
Simple YouTube View Generator
Usage: python run_simulation.py <video_url> <view_count>
"""

import sys
import logging
from src.view_generator import ViewGenerator

def main():
    if len(sys.argv) != 3:
        print("Usage: python run_simulation.py <video_url> <view_count>")
        print("Example: python run_simulation.py 'https://youtube.com/watch?v=abc123' 1000")
        sys.exit(1)

    video_url = sys.argv[1]
    try:
        view_count = int(sys.argv[2])
    except ValueError:
        print("Error: view_count must be a number")
        sys.exit(1)

    if view_count <= 0:
        print("Error: view_count must be positive")
        sys.exit(1)

    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('views.log'),
            logging.StreamHandler()
        ]
    )

    # Create and run generator
    generator = ViewGenerator()
    generator.generate_views(video_url, view_count)

if __name__ == "__main__":
    main()