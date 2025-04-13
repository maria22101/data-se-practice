import json
import os
from typing import List, Dict, Any


def save_to_disk(json_content: List[Dict[str, Any]], dir_path: str, file_name: str) -> None:
    file_path = os.path.join(dir_path, file_name)
    dirname = os.path.dirname(file_path)
    os.makedirs(dirname, exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_content, json_file, ensure_ascii=False, indent=4)
