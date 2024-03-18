import hashlib

def convert_to_hashes(input_file, output_file, input_encoding='utf-8'):
    with open(input_file, 'r', encoding=input_encoding) as f:
        words = f.read().splitlines()

    with open(output_file, 'w') as f:
        for word in words:
            sha256_hash = hashlib.sha256(word.encode()).hexdigest()
            f.write(f"{sha256_hash}:{word}\n")

# Example usage
input_file = 'rockyou.txt'
output_file = 'hashed_words.txt'
input_encoding = 'latin-1'  # Change this to the appropriate encoding

convert_to_hashes(input_file, output_file, input_encoding)