"""Settings for the portfolio server.

Add a folder name to EXCLUDED_FOLDERS when it should not appear on the site.
Names are matched against top-level folders next to SERVER.
"""

EXCLUDED_FOLDERS = {
    "100 Days of Code - The Complete Python Pro Bootcamp",
}

# Projects that are too small, unfinished, or not ready to share can be
# listed here without deleting them from the repository.
EXCLUDED_PROJECTS = set()

RUN_TIMEOUT_SECONDS = 8
MAX_OUTPUT_CHARACTERS = 12_000
