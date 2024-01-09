ef split_file_if_needed(file_path, char_limit=4000):
    """Splits the file into multiple parts without truncating domain names."""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    new_files = []
    current_content = ""
    part_number = 1

    for line in lines:
        if len(current_content) + len(line) > char_limit:
            # Save current content to a new file
            new_file_path = f"{os.path.splitext(file_path)[0]}_part{part_number}.txt"
            with open(new_file_path, 'w', encoding='utf-8') as new_file:
                new_file.write(current_content)
            new_files.append(new_file_path)

            # Start new content and increment part number
            current_content = line
            part_number += 1
        else:
            current_content += line

    # Save the last part if there's any content left
    if current_content:
        new_file_path = f"{os.path.splitext(file_path)[0]}_part{part_number}.txt"
        with open(new_file_path, 'w', encoding='utf-8') as new_file:
            new_file.write(current_content)
        new_files.append(new_file_path)

    return new_files