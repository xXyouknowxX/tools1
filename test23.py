def split_file_if_needed(file_path):
    """Splits the file into two if it exceeds 4000 ASCII characters."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    if len(content) > 4000:
        half_way_point = len(content) // 2
        part1 = content[:half_way_point]
        part2 = content[half_way_point:]

        base_name = os.path.basename(file_path)
        file_part1_path = f"{base_name}_part1.txt"
        file_part2_path = f"{base_name}_part2.txt"

        with open(file_part1_path, 'w', encoding='utf-8') as file1:
            file1.write(part1)
        with open(file_part2_path, 'w', encoding='utf-8') as file2:
            file2.write(part2)

        return file_part1_path, file_part2_path
    else:
        return file_path,

def read_targets_from_file(file_path):
    """Reads IP addresses and FQDNs from a file."""
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    fqdn_pattern = r'\b(?:[a-zA-Z\d-]{,63}\.)+[a-zA-Z]{2,63}\b'

    ips, fqdns = [], []
    file_paths = split_file_if_needed(file_path)
    for path in file_paths:
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
            ips.extend([line for line in lines if re.fullmatch(ip_pattern, line)])
            fqdns.extend([line for line in lines if re.fullmatch(fqdn_pattern, line)])

    return ','.join(ips), ','.join(fqdns)