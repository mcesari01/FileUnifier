# File Unifier Tool

## Description

The **File Unifier Tool** is a Python desktop application with a graphical interface (GUI) built using Tkinter. It allows you to select multiple source files—even from different folders—and merge their contents into a single, unified text file.

This tool is especially useful for sharing multiple code or text files (e.g., when working with AI models like ChatGPT), giving a clear and complete view of your working environment in a single document.

## Features

- Select multiple files from different directories (no folder restriction)
- Easily add or remove files from the selection list
- Preview the merged content directly in the application
- Merge selected files into a single output file, with filename of your choice
- Merge content includes file separators for clarity: # Start of file: filename.py
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
