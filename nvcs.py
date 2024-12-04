#!/usr/bin/env python

import json
import os
import argparse
import subprocess
import sys


CONFIG_FILE_PATH = os.path.expanduser("~/.config/nv-config/configs.json")


def load_configs():
    """
    Load configurations from a JSON file.
    If the file does not exist, return an empty dictionary.
    """
    if not os.path.exists(CONFIG_FILE_PATH):
        return {}
    with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_configs(configs: dict):
    """
    Save configurations to a JSON file.
    If the directory does not exist, create it.
    """
    os.makedirs(os.path.dirname(CONFIG_FILE_PATH), exist_ok=True)
    with open(CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(configs, f, indent=4)


def list_configs(configs: dict):
    """
    List available configurations.
    If there are no configurations, print a message.
    """
    if not configs:
        print("No configurations found.")
    else:
        for i, (name, folder) in enumerate(configs.items(), 1):
            print(f"{i}. {name}: {folder}")


def add_config(configs: dict):
    """
    Add a new configuration.
    Prompt the user for the name and folder name.
    Save the configuration to the JSON file.
    """
    name = input("Enter configuration name: ")
    folder = input("Enter config folder name in .config (e.g., nvim-lazyvim): ")
    configs[name] = folder
    save_configs(configs)
    print(f"Configuration '{name}' added.")


def remove_config(configs: dict):
    """
    Remove an existing configuration.
    Prompt the user to select a configuration to remove.
    Remove the selected configuration from the JSON file.
    """
    list_configs(configs)
    index = int(input("Enter number to remove: ")) - 1
    if 0 <= index < len(configs):
        name = list(configs.keys())[index]
        del configs[name]
        save_configs(configs)
        print(f"Configuration '{name}' removed.")
    else:
        print("Invalid selection.")


def choose_config(configs: dict, target: str, config_num: int = None):
    """
    Choose and use a configuration.
    If config_num is provided, use that configuration directly.
    Otherwise, prompt the user to select a configuration.
    Set the NVIM_APPNAME environment variable to the selected folder name.
    Open the target file or directory with Neovim.
    """
    if not configs:
        print("No configurations available.")
        return

    if config_num != "" and config_num is not None:
        # Adjust for 0-based indexing
        index = config_num - 1
        if 0 <= index < len(configs):
            _set_nvim_appname(configs, index, target)
        else:
            print(
                f"Invalid configuration number. Please choose between 1 and {len(configs)}"
            )
            list_configs(configs)
        return
    else:
        list_configs(configs)
        index = int(input("Choose configuration by number: ")) - 1
        if 0 <= index < len(configs):
            _set_nvim_appname(configs, index, target)
        else:
            print("Invalid selection.")


def _set_nvim_appname(configs, index, target):
    """
    Set the NVIM_APPNAME environment variable to the selected folder name.
    Open the target file or directory with Neovim.
    """
    config_folder = list(configs.values())[index]
    os.environ["NVIM_APPNAME"] = config_folder
    subprocess.run(["nvim", target], check=True)


def init_configs(configs: dict):
    """
    Initialize configurations by scanning ~/.config directory.
    Add found configurations to the JSON file.
    """
    print("Starting initialization...")
    config_dir = os.path.expanduser("~/.config")
    print(f"Searching in directory: {config_dir}")
    found_configs = False

    try:
        folders = os.listdir(config_dir)
        print(f"Found {len(folders)} folders to check")
        for folder in folders:
            print(f"Checking folder: {folder}")
            if "nvim" in folder.lower():
                configs[folder] = folder
                print(f"Configuration '{folder}' added.")
                found_configs = True

        if not found_configs:
            print("No Neovim configurations found in ~/.config directory.")
        else:
            save_configs(configs)
            print("Configurations saved successfully.")
    except Exception as e:
        print(f"Error during initialization: {e}")


def main():
    """
    Main function for the Neovim Config Switcher script.
    Parse command line arguments and execute the appropriate command.
    """
    parser = argparse.ArgumentParser(
        description="Neovim Config Switcher - A tool to manage multiple Neovim configurations"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    add_parser = subparsers.add_parser("add", help="Add a new configuration")  # t

    remove_parser = subparsers.add_parser(
        "remove", help="Remove an existing configuration"
    )

    list_parser = subparsers.add_parser(
        "list", help="List all available configurations"
    )

    init_parser = subparsers.add_parser(
        "init", help="Initialize configurations by scanning ~/.config directory"
    )

    choose_parser = subparsers.add_parser(
        "choose", help="Choose and use a configuration"
    )
    choose_parser.add_argument(
        "target",
        nargs="?",
        help="Target file or directory to open with the chosen configuration",
    )
    choose_parser.add_argument(
        "-n",
        "--number",
        type=int,
        help="Configuration number to use (bypasses selection prompt)",
    )

    args = parser.parse_args()

    configs = load_configs()

    if args.command == "add":
        add_config(configs)
    elif args.command == "remove":
        remove_config(configs)
    elif args.command == "list":
        list_configs(configs)
    elif args.command == "init":
        init_configs(configs)
        list_configs(configs)
    elif args.command == "choose":
        if args.target:
            choose_config(configs, args.target, args.number)
        else:
            print("Please provide a target file or directory.")
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
