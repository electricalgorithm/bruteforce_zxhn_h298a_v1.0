def divide_file_into_parts(input_file, num_parts):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    chunk_size = len(lines) // num_parts
    chunks = [lines[i:i + chunk_size]
              for i in range(0, len(lines), chunk_size)]

    for i, chunk in enumerate(chunks):
        with open(f'part{i+1}.txt', 'w') as f:
            f.writelines(chunk)


if __name__ == "__main__":
    input_file = 'wordlist.txt'  # replace with your input file name
    divide_file_into_parts(input_file, 5)
