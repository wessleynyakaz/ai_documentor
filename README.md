# AI CODE BASE DOCUMENTOR

Automatically generated documentation for your codebase

## Environment Setup

Create a `.env` file with the following variables:

```
OPENAI_API_KEY="...your API key..."
ROOT_DIR="root dir of code base"
```

## Running the Script

Run the following command in your terminal:

```
clear && python auto_documentation.py
```

This will document the `manage.py` file for now. Additional support will be added in the future.

## Code Overview

The code includes the following main components:

### 1. Parsing Code

The `parse_code` function takes a code snippet as input and extracts relevant information, such as function names and parameters, using the `ast` module.

### 2. Generating Comments

The `generate_comments` function uses the OpenAI GPT model to generate comments and documentation for a given code snippet. It includes a retry loop with exponential backoff to handle rate limit errors.

### 3. Traversing the Codebase

The `process_codebase` function recursively traverses the codebase directory, reads the code from each file, and generates comments/documentation using the `generate_comments` function. Currently, it only processes the `manage.py` file, but you can add support for more file types as needed.

### 4. Main Function

The `main` function is the entry point of the script. It retrieves the root directory of the codebase from the environment variable `ROOT_DIR` and calls the `process_codebase` function.

## Usage

1. Ensure you have the necessary environment variables set in the `.env` file.
2. Run the script using the command `clear && python auto_documentation.py`.
3. The script will process the `manage.py` file and generate comments/documentation, which will be written back to the file.
