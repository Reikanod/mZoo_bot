with open(r'../ya_api_keys.txt', 'r', encoding='utf-8') as file:
    file_lines = file.readlines()
    cat_id = file_lines[1].strip()
    ya_api_id = file_lines[5].strip()
