#!/usr/bin/env python3

"""Main Entry point for the package

Author(s)
---------
Daniel Gisolfi <Daniel.Gisolfi1@marist.edu>

Usage
-----
    python3 -m template
"""

from VibeBot import __project_urls__
from VibeBot.server import server


def main():
    server.run(host="0.0.0.0", port=5080, debug=False)


if __name__ == "__main__":
    main()
