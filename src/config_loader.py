
import json
import sys


def load_config():

    try:
        with open("config.json", "r", encoding="utf-8") as file:

            config = json.load(file)

            print("Configuration loaded successfully!")

            return config

    except FileNotFoundError:
        print("Error: config.json file not found.")
        sys.exit(1)

    except json.JSONDecodeError:
        print("Error: Invalid JSON format in config.json.")
        sys.exit(1)
