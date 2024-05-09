from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import Dict, Any
from openai import OpenAI
import ast
import time
import random


import openai

# Load environment variables from .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
# Function to parse code and extract relevant information


def parse_code(code: str) -> Dict[str, Any]:
    # Initialize an empty dictionary to store extracted information
    extracted_info = {}

    # Parse code using ast module
    tree = ast.parse(code)

    # Traverse the abstract syntax tree to extract relevant information
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):  # If node is a function definition
            function_name = node.name
            parameters = [arg.arg for arg in node.args.args]
            # You can extract more information as needed (e.g., return type, docstring)
            # Add extracted information to the dictionary
            extracted_info[function_name] = {'parameters': parameters}

    return extracted_info

# Function to generate comments using OpenAI's GPT model


# Function to generate comments using DeepAI's GPT model
def generate_comments(code_snippet, retry_count=3):
    # Set up prompt with code snippet
    prompt = f"Given the following code snippet:\n\n{code_snippet}\n\nGenerate comments/documentation for this code:"
    print(f'prompt:\n\n{prompt}\n')

    # Retry loop with exponential backoff
    for attempt in range(retry_count):
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages= [
                    {
                        "role" : "system",
                        "content" : prompt
                    }
                ]
            )
            # Extract generated comments from response
            generated_comments = response.choices[0].text.strip()
            print(f'Generated comments: {generated_comments}')
            return generated_comments
        except openai.RateLimitError as e:
            # Exponential backoff
            delay = 2 ** attempt + random.uniform(0, 1)
            print(f"Rate limit exceeded. Retrying in {delay} seconds.")
            time.sleep(delay)

    # If all retries fail, raise an exception
    raise RuntimeError("Failed to generate comments after multiple retries.")

# Function to traverse codebase directory and process files


def process_codebase(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            # Add more supported extensions as needed
            if filename.endswith('manage.py'):
                file_path = os.path.join(dirpath, filename)
                print("FILE: %s" % file_path)
                # Read code from file
                with open(file_path, 'r') as file:
                    code = file.read()
                # Parse code and extract relevant information
                extracted_info = parse_code(code)
                # Generate comments/documentation using DeepAI's GPT model
                generated_comments = generate_comments(code)
                # Rewrite file with generated comments/documentation
                with open(file_path, 'w') as file:
                    # Write generated comments to file
                    file.write(generated_comments)

# Main function


def main():
    root_dir = os.getenv('ROOT_DIR')
    print('Root directory: %s' % root_dir)
    process_codebase(root_dir)


if __name__ == "__main__":
    print("Running command")
    main()
