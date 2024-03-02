import json

def calculate_tokens(text):
    # Assuming 4 characters = 1 token
    return len(text) / 4

def process_file(input_filename):
    with open(input_filename, 'r', encoding='utf-8') as infile:
        line_number = 0
        over_510_token_lines_count = 0  # Counter for lines with more than 510 tokens
        for line in infile:
            line_number += 1
            try:
                data = json.loads(line)  # Convert JSON string to dictionary
                query = data.get("query", "")
                relevant_passages = " ".join(data.get("relevant_passages", []))
                full_text = query + " " + relevant_passages
                tokens = calculate_tokens(full_text)
                
                if tokens > 510:
                    over_510_token_lines_count += 1
                    print(f"Line {line_number} exceeds 510 tokens: {tokens} tokens")
            except json.JSONDecodeError as e:
                print(f"Skipping line {line_number}: Unable to parse JSON. Error: {e}")
        
        # After processing all lines, print the total number of lines with more than 510 tokens
        print(f"Total number of lines with more than 510 tokens: {over_510_token_lines_count}")

# Replace 'cleaned_data.jsonl' with the path to your input file
input_filename = '/home/danledger/reranker/cleaned_data.jsonl'
process_file(input_filename)
