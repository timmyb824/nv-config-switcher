#!/usr/bin/env python

import json
import os
import logging
import subprocess
import sys

CONFIG_FILE = os.path.expanduser("~/.config/nv-config/configs.json")


def load_configs():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_configs(configs):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(configs, f, indent=4)


def list_configs(configs):
    if not configs:
        print("No configurations found.")
    else:
        for i, (name, folder) in enumerate(configs.items(), 1):
            print(f"{i}. {name}: {folder}")


def add_config(configs):
    name = input("Enter configuration name: ")
    folder = input("Enter config folder name in .config (e.g., nvim-lazyvim): ")
    configs[name] = folder
    save_configs(configs)
    print(f"Configuration '{name}' added.")


def remove_config(configs):
    list_configs(configs)
    index = int(input("Enter number to remove: ")) - 1
    if 0 <= index < len(configs):
        name = list(configs.keys())[index]
        del configs[name]
        save_configs(configs)
        print(f"Configuration '{name}' removed.")
    else:
        print("Invalid selection.")


def choose_config(configs, target):
    if not configs:
        print("No configurations available.")
        sys.exit(1)

    list_configs(configs)
    index = int(input("Choose configuration by number: ")) - 1
    if 0 <= index < len(configs):
        config_folder = list(configs.values())[index]
        os.environ["NVIM_APPNAME"] = config_folder
        subprocess.run(["nvim", target], check=True)
    else:
        print("Invalid selection.")


def init_configs(configs):
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
    configs = load_configs()
    if len(sys.argv) < 2:
        print("Usage: nv-config [add|remove|list|init|<file|directory>]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "add":
        add_config(configs)
    elif command == "remove":
        remove_config(configs)
    elif command == "list":
        list_configs(configs)
    elif command == "init":
        init_configs(configs)
        list_configs(configs)  # Show the configs after initialization
    else:
        target = command
        choose_config(configs, target)


if __name__ == "__main__":
    main()
