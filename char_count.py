def count_characters_in_file(filename):
    total_characters = 0
    with open(filename, 'r') as file:
        for line in file:
            total_characters += len(line)  # Count the characters in each line
    return total_characters

# Replace 'data.jsonl' with the path to your file
filename = '/home/danledger/reranker/data_no_foo.jsonl'
total_characters = count_characters_in_file(filename)
print(f"Total number of characters in {filename}: {total_characters}")
