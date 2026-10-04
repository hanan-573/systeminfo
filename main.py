"""
main.py - Main entry point for the system information tool.
Runs in a loop, refreshing data every 2 seconds until Ctrl+C.
"""
import sys
import time
import os
import traceback
from systemdetection import get_all_info
from interface import print_header, display_info, print_error, clear_screen


def main():
    """Continuously fetch and display system information until interrupted."""
    try:
        refresh_interval = 2  # seconds

        while True:
            clear_screen()
            print_header()
            print("Press Ctrl+C to exit\n")
            info = get_all_info()
            display_info(info)
            time.sleep(refresh_interval)

    except KeyboardInterrupt:
        print_error("\nExited by user.")
        sys.exit(0)
    except Exception as e:
        print_error(f"An unexpected error occurred: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()