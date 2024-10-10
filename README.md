# File Unifier Tool

## Description

The **File Unifier Tool** is a Python application built using Tkinter that allows users to search for and merge files with specified extensions from a selected folder. The contents of the files are concatenated and saved into a single output file.

This tool is particularly useful when you need to send multiple files to ChatGPT, allowing the model to understand the full context of the environment you are working in by combining several files into one for easier sharing.

## Features

- Select a folder containing the files to be merged.
- Choose one or more file extensions to search for (e.g., `.py`, `.txt`, `.java`, etc.).
- Merge the contents of all found files into a single text file.
- View the unified content directly within the graphical interface.
- Save the merged content to a single output file with a custom name.

## Requirements

- Python 3.x
- Required libraries:
  - `tkinter` (for the graphical user interface)
  - `threading` (to handle the merge process in a separate thread)

## Installation

1. Ensure that Python 3 is installed on your system.
2. Clone or download this repository.
3. Install the necessary dependencies:

   ```bash
   pip install tk
