import os
import json
from dotenv import load_dotenv
from groq import Groq 
from tqdm import tqdm

# Load environment variables
load_dotenv()

# Initialize Groq client
groq_client = Groq(
    api_key=os.environ["GROQ_API_KEY"],
)
llama = 'llama3-8b-8192'

# Function to call your language model API for generating query variants
def generate_response(query, relevant_chunk):
    instructions = (
        "You're a very experienced customer support agent working for Ledger, the crypto hardware wallet company. "
        "Using your knowledge of cryptocurrency, blockchains, and Ledger products (Ledger Nano S, Nano S Plus, Nano X, Ledger Stax, Ledger Recover and Ledger Live), provide a friendly answer to this query from a Ledger customer: "
        f'QUERY:\n """"{query}""""\n'
        "Always use this relevant information from the Ledger Help Center to inform your answer to the query: "
        f'"{relevant_chunk}" \n'
        "Your response should ALWAYS be in the following .json format as follows and without anything else or any added information: '{\"1\":\"<your response>\"}'"
        "Avoid using special characters such as emojis or CSS characters."
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

    # JSON parsing is expected to be correct from the server
    try:
        response_content = json.loads(response_text)
        if '1' in response_content:
            return [response_content['1']]
        elif 'response' in response_content:
            return [response_content['response']]
        else:
            print("Unexpected JSON format:", response_text)
            return []
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e)
        return []

# Main function to process the jsonl file and generate synthetic variants
def process_jsonl_file(input_filepath, output_filepath):
    synthetic_data = []
    with open(input_filepath, "r") as file:
        lines = file.readlines()  # Read lines once to use them with tqdm
        for line in tqdm(lines, desc="Processing JSON Lines"):
            original_data = json.loads(line)
            original_query = original_data['query']
            relevant_chunk = original_data['relevant_passages'][0]
            query_responses = generate_response(original_query, relevant_chunk)

            # Append synthetic data
            for response in query_responses:
                synthetic_entry = {
                    'query': original_query,
                    'response': response
                }
                print(synthetic_entry)
                synthetic_data.append(json.dumps(synthetic_entry))

    # Write synthetic data to a new JSONL file
    with open(output_filepath, "w") as outfile:
        for entry in synthetic_data:
            outfile.write(entry + "\n")

# Example usage
input_file = '/home/danledger/reranker/trimmed_data.jsonl'
output_file = '/home/danledger/reranker/synthetic_answers.jsonl'
process_jsonl_file(input_file, output_file)