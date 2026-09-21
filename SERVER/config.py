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

# The text here is shown to visitors before they run a project. Add a new
# entry when a newly discovered project needs custom instructions.
PROJECT_GUIDES = {
    "Day 16": {
        "title": "Coffee machine",
        "description": "Order coffee, inspect the machine report, and pay with virtual coins.",
        "instructions": (
            "Enter one response at a time. Start with espresso, latte, or "
            "cappuccino. For a drink, provide four whole-number coin counts "
            "in this order: quarters, dimes, nickles, pennies. Use report "
            "to inspect the machine or off to finish."
        ),
        "example_input": "latte\n10\n0\n0\n0\noff\n",
        "prompt_pattern": r"(?:What would you like\?.*:|How many .*?:)$",
    },
    "Day 17": {
        "title": "True or false quiz",
        "description": "Answer the 12 general-knowledge questions and see your score.",
        "instructions": (
            "Enter True or False for the current question. The quiz prints the "
            "question before reading each answer and ends after question 12."
        ),
        "example_input": "True\nFalse\nTrue\nTrue\nTrue\nFalse\nTrue\nFalse\nTrue\nTrue\nFalse\nTrue\n",
        "prompt_pattern": r"Q\d+: .* \(True/False\)$",
    },
    "Day 24": {
        "title": "Mail merge",
        "description": "Creates a personalized letter for every name in the input file.",
        "instructions": (
            "This project needs no input. Run it to replace [name] in the "
            "template and write letters into Output/ReadyToSend."
        ),
        "example_input": "",
    },
    "Day 26": {
        "title": "NATO phonetic alphabet",
        "description": "Converts a word into its NATO phonetic alphabet code words.",
        "instructions": (
            "Enter one word containing letters A-Z. The project prints the "
            "phonetic dictionary and then the code words for your input."
        ),
        "example_input": "hello\n",
        "prompt_pattern": r"Enter a word: $",
    },
    "Day 30": {
        "title": "NATO phonetic alphabet (validated)",
        "description": "Converts a word into NATO code words and rejects non-letter input.",
        "instructions": (
            "Enter a word containing only letters A-Z. Invalid input is "
            "rejected and the project asks again until a valid word is entered."
        ),
        "example_input": "python\n",
        "prompt_pattern": r"Enter a word: $",
    },
}
