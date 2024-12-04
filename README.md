# Neovim Config Switcher (nvcs)

A simple command-line tool to manage and switch between multiple Neovim configurations.

## Overview

nvcs (Neovim Config Switcher) allows you to easily manage and switch between different Neovim configurations by leveraging Neovim's `NVIM_APPNAME` environment variable. This is particularly useful if you maintain multiple Neovim setups (e.g., one for minimal editing, another for full IDE features).

## Installation

1. Clone this repository:

```bash
git clone https://github.com/timmyb824/nv-config-switcher.git
```

2. Move the `nvcs.py` script to a location in your PATH and make it executable:

```bash
# Example
cp nv-config-switcher/nvcs.py ~/.local/bin/nvcs
chmod +x ~/.local/bin/nvcs
```

## Usage

The script provides several commands to manage your Neovim configurations:

### Initialize Configurations

Automatically scan your `~/.config` directory for Neovim configurations:

```bash
nvcs init
```

### List Configurations

View all available configurations:

```bash
nvcs list
```

### Add a Configuration

Add a new configuration manually:

```bash
nvcs add
```

### Remove a Configuration

Remove an existing configuration:

```bash
nvcs remove
```

### Choose and Use a Configuration

Open a file or directory with a specific Neovim configuration:

```bash
# Interactive mode
nvcs choose <file_or_directory>

# Direct selection mode
nvcs choose <file_or_directory> -n <config_number>
```

## Configuration Storage

The tool stores configuration information in `~/.config/nv-config/configs.json`. Each configuration entry maps a friendly name to its corresponding directory name in `.config`.

## Requirements

- Python 3.11 or higher
- Neovim installed with one or more configurations in `~/.config`
  - For automatically scanning configurations with `nvcs init`, the folder name must contain the word "nvim" in it.

## Future Plans

- Package distribution via pip
- Additional configuration management features

## Contributing

Feel free to open issues or submit pull requests with improvements.

## License

MIT License
