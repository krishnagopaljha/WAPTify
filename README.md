# WAPTify

A CLI-based security testing tool with modular architecture for web application vulnerability assessment.

![CLI Tool Demo](https://img.shields.io/badge/CLI-Tool-brightgreen) 
![Python](https://img.shields.io/badge/Python-3.6%2B-blue)


## Features

- **JWT Operations**
  - Encode/decode JSON Web Tokens
  - File input/output support
  - HS256 algorithm support
- **Parameter Discovery**
  - Wordlist-based fuzzing
  - GET/POST method support
  - Multi-threaded scanning
- **Vulnerability Scanners**
  - XSS Detection (with custom payload support)
  - Local File Inclusion (LFI) Testing
  - Open Redirect Detection
- **Directory Bruteforcing**
  - Multi-threaded implementation
  - Custom wordlist support
- **Modular Architecture**
  - Easy to extend and modify
  - Clean code separation


## Requirements

- Python 3.x
- Required Python packages are listed in `requirements.txt`.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/krishnagopaljha/WAPTify.git
   cd osint
   ```
2. **Install Dependenciesy**

   Install the required Python packages using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

   ## Usage

   1. Run the Tool

      Execute app.py to start the interactive mode:

      ```bash
      python WAPTify.py
      ```
