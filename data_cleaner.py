import json

def replace_foo_in_dict(d):
    """Recursively replaces 'foo' with an empty string in a dictionary."""
    for k, v in d.items():
        if isinstance(v, dict):
            replace_foo_in_dict(v)
        elif isinstance(v, list):
            for i in range(len(v)):
                if isinstance(v[i], dict):
                    replace_foo_in_dict(v[i])
                elif isinstance(v[i], str):
                    v[i] = v[i].replace('foo', '').replace('\n', '').replace('“', '').replace('”', '').replace('’', '')
        elif isinstance(v, str):
            d[k] = v.replace('foo', '').replace('\n', '').replace('“', '').replace('”', '').replace('’', '')

def process_file(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as infile, open(output_filename, 'w', encoding='utf-8') as outfile:
        line_number = 0
        for line in infile:
            line_number += 1
            try:
                data = json.loads(line)  # Convert JSON string to dictionary
                replace_foo_in_dict(data)  # Replace 'foo' with ''
                json_line = json.dumps(data, ensure_ascii=False)  # Convert dictionary back to JSON string
                
                # Since the line replacements are now handled in replace_foo_in_dict, we directly write the modified line
                outfile.write(json_line + '\n')
            except json.JSONDecodeError as e:
                print(f"Skipping line {line_number}: Unable to parse JSON. Error: {e}")

# Replace 'input.jsonl' with the path to your input file and 'output.jsonl' for the output file name
input_filename = '/home/danledger/reranker/data.jsonl'
output_filename = 'cleaned_data.jsonl'
process_file(input_filename, output_filename)

print(f"Processed file saved as {output_filename}")
