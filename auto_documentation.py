import os
from dotenv import load_dotenv
from typing import Dict, Any
import ast
import openai

# Load environment variables from .env file
load_dotenv()

# Set up your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

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


def generate_comments(code_snippet):
    # Set up prompt with code snippet
    prompt = f"Given the following code snippet:\n\n{code_snippet}\n\nGenerate comments/documentation for this code:"
    # Call OpenAI's completion endpoint
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150  # Adjust as needed
    )
    # Extract generated comments from response
    generated_comments = response.choices[0].text.strip()
    return generated_comments

# Function to traverse codebase directory and process files


def process_codebase(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            # Add more supported extensions as needed
            if filename.endswith(('.py', '.tsx')):
                file_path = os.path.join(dirpath, filename)
                # Read code from file
                with open(file_path, 'r') as file:
                    code = file.read()
                # Parse code and extract relevant information
                extracted_info = parse_code(code)
                # Generate comments/documentation using OpenAI's GPT model
                generated_comments = generate_comments(code)
                # Rewrite file with generated comments/documentation
                with open(file_path, 'w') as file:
                    # Write generated comments to file
                    file.write(generated_comments)


# Main function


def main():
    root_dir = os.getenv('ROOT_DIR')
    process_codebase(root_dir)


if __name__ == "__main__":
    print("Running command")
    main()
