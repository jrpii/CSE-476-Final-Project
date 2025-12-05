### Utility functions for data loading, parsing, evaluation, and the agent loop.
import json
from typing import Dict, List, Any

# Helper method to extract json data as a dictionary.
def parse_json_input(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Extract input & output, domain (if present)
    parsed = []
    for item in data:
        parsed_field = {"input": item["input"]}
        if "output" in item:
            parsed_field["output"] = item["output"]
        if "domain" in item:
            parsed_field["domain"] = item["domain"]
        parsed.append(parsed_field)
    
    return parsed
