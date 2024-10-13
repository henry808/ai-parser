#!/usr/bin/env python
# file_processor.py
#
# Example: ./file_processor.py --input input.txt --output output.txt
# Display Help: ./file_processor.py -h
# Check Version: ./file_processor.py --version
#
# 
# ./ai_processor.py -i test_input.txt -o test_output.txt

# ai_processor.py
import re

def clean_text(text: str) -> str:
    """
    Cleans up the text by replacing escaped quotes with standard quotes
    and expanding newline characters into actual end-of-line characters.
    
    Args:
        text (str): The text to clean.

    Returns:
        str: Cleaned text.
    """
    # Replace escaped quotes with regular quotes
    cleaned_text = text.replace('\\"', '"')
    # Replace escaped newlines with actual newlines
    cleaned_text = cleaned_text.replace('\\n', '\n')

    # Use a regex to reduce multiple spaces between words (not touching newlines or tabs)
    cleaned_text = re.sub(r'(?<=\S) {2,}(?=\S)', ' ', cleaned_text)

    # Trim leading and trailing spaces for each line
    cleaned_text = '\n'.join([line.strip() for line in cleaned_text.splitlines()])

    # Ensure no more than two consecutive newlines (reduce multiple newlines to double newlines)
    cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)

    return cleaned_text

def process_file(file_path: str):
    """
    Processes the input file to extract system_instruction, user messages, and model messages.
    
    Args:
        file_path (str): The path to the input file.

    Returns:
        tuple: A tuple containing the system_instruction (str), user_list (list), and model_list (list).
    """
    system_instruction = ""
    user_list = []
    model_list = []

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")

    in_user_message = False
    in_model_message = False

    for i, line in enumerate(lines):
        line = line.strip()

        print(f"Looking at line: {line[:20]}")  # Debugging line

        # Check for system_instruction and extract it
        if '"system_instruction":' in line:
            print(f"Found system_instruction line: {line[:20]}")  # Debugging line
            start_idx = line.find('"', line.find('"system_instruction":') + len('"system_instruction": ')) + 1
            end_idx = line.rfind('"')
            system_instruction = clean_text(line[start_idx:end_idx])
            print(f"Extracted system_instruction: {system_instruction[:20]}")  # Debugging line
        
        # Detect user message and mark the next line for parts extraction
        elif '"role": "user"' in line:
            in_user_message = True
            print(f"Found user role: {line[:20]}")  # Debugging line
        
        # Detect model message and mark the next line for parts extraction
        elif '"role": "model"' in line:
            in_model_message = True
            print(f"Found model role: {line[:20]}")  # Debugging line

        # Extract user message after "parts"
        elif in_user_message and '"parts": [' in line:
            # Move to the next line to get the actual message
            message_line = lines[i+1].strip()
            print(f"Found user parts line: {message_line[:20]}")  # Debugging line
            start_idx = message_line.find('"') + 1
            end_idx = message_line.rfind('"')
            user_message = clean_text(message_line[start_idx:end_idx])
            user_list.append(user_message)
            print(f"Extracted user message: {user_message[:20]}")  # Debugging line
            in_user_message = False  # Reset the flag after extraction

        # Extract model message after "parts"
        elif in_model_message and '"parts": [' in line:
            # Move to the next line to get the actual message
            message_line = lines[i+1].strip()
            print(f"Found model parts line: {message_line[:20]}")  # Debugging line
            start_idx = message_line.find('"') + 1
            end_idx = message_line.rfind('"')
            model_message = clean_text(message_line[start_idx:end_idx])
            model_list.append(model_message)
            print(f"Extracted model message: {model_message[:20]}")  # Debugging line
            in_model_message = False  # Reset the flag after extraction

    return system_instruction, user_list, model_list

def format_output(system_instruction: str, user_list: list, model_list: list, mode: str) -> str:
    """
    Formats the extracted information into the desired output format.
    
    Args:
        system_instruction (str): The system instruction.
        user_list (list): List of user messages.
        model_list (list): List of model messages.
        mode (str): The selected mode for formatting ('prose' or 'exchange').

    Returns:
        str: The formatted output.
    """
    output_lines = []

    # Add the system instruction in both modes
    output_lines.append(f'Instructions: "{clean_text(system_instruction)}"')

    # Mode 'prose': Only include model messages with no header
    if mode == 'prose':
        for model_message in model_list:
            output_lines.append(clean_text(model_message))
    
    # Mode 'exchange': Alternate between user and model with headers
    elif mode == 'exchange':
        for i in range(len(user_list)):
            output_lines.append(f'User: "{clean_text(user_list[i])}"')
            if i < len(model_list):
                output_lines.append(f'Model: {clean_text(model_list[i])}')

    return '\n\n'.join(output_lines)

def main(args):
    # Extract system_instruction, user messages, and model messages
    system_instruction, user_list, model_list = process_file(args.input)

    # Format the output based on the selected mode
    final_output = format_output(system_instruction, user_list, model_list, args.mode)

    # Write the output to the output file
    with open(args.output, 'w') as outfile:
        outfile.write(final_output)

if __name__ == "__main__":
    # Parse arguments using the existing parser
    from parser import create_parser
    parser = create_parser()
    args = parser.parse_args()
    main(args)
