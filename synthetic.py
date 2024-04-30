from tqdm import tqdm
import json
import requests
import os
from dotenv import load_dotenv
from groq import Groq

# Initialize environment variables
load_dotenv()

# Initialize Groq client
groq_client = Groq(
    api_key=os.environ["GROQ_API_KEY"],
)
llama = 'llama3-8b-8192'

# Function to call your language model API for generating query variants
def generate_query_variants(query):
    instructions = (
        f"Generate 5 variants of this query: '{query}'\n\n"
        "Your response should ALWAYS be in .json format as follows and without anything else:\n\n"
        '{{"1":"<the first variant>",\n'
        ' "2":"<the second variant>",\n'
        ' "3":"<the third variant>",\n'
        ' "4":"<the fourth variant>",\n'
        ' "5":"<the fifth variant>"}}\n'
    )
    res = groq_client.chat.completions.create(
        temperature=0.4,
        model=llama,
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": query}
        ],
        timeout=45.0
    )
    response_text = res.choices[0].message.content
    print("API Response before checking:", response_text)  # Log the output to verify it's correct

    # Ensure the response ends with a closing curly brace
    if not response_text.strip().endswith('}'):
        response_text += '}'
        print("Malformed JSON corrected")

    try:
        response_content = json.loads(response_text)
        return [response_content[str(i)] for i in range(1, 6)]
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e)
        return []

# Main function to process the jsonl file and generate synthetic variants
def process_jsonl_file(input_filepath, output_filepath):
    synthetic_data = []
    with open(input_filepath, "r") as file:
        lines = file.readlines()  # Read lines once to use them with tqdm
        for line in tqdm(lines, desc="Processing JSON Lines"):  # Add tqdm progress bar
            original_data = json.loads(line)
            query_variants = generate_query_variants(original_data['query'])

            # Append original data
            synthetic_data.append(json.dumps(original_data))  # Original line
            for variant in query_variants:
                synthetic_entry = {
                    'query': variant,
                    'relevant_passages': original_data.get('relevant_passages', []),
                    'hard_negatives': original_data.get('hard_negatives', [])
                }
                synthetic_data.append(json.dumps(synthetic_entry))

    # Write synthetic data to a new JSONL file
    with open(output_filepath, "w") as outfile:
        for entry in synthetic_data:
            outfile.write(entry + "\n")

# Example usage
input_file = '/home/danledger/reranker/trimmed_data.jsonl'
output_file = '/home/danledger/reranker/synthetic.jsonl'
process_jsonl_file(input_file, output_file)
