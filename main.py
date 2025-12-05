### Main script, will eventually be entry point for agent loop.
import sys
import argparse
from scripts.config import get_api_key, get_api_base, get_model_name
from src.utils import parse_json_input

# Address Unicode encoding for Windows (keep parsed data unchanged.)
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

API_KEY = get_api_key()
API_BASE = get_api_base()
MODEL = get_model_name()

def main():
    # For now, just test parsing of json.
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Path to JSON file for agent to parse.")
    parser.add_argument("--max", type=int, default=None, help="Max entries to process")
    
    args = parser.parse_args()
    
    data = parse_json_input(args.input)
    
    if args.max is not None:
        data = data[:args.max]
    
    print(f"Loaded {len(data)} entries.\n")
    
    for idx, entry in enumerate(data):
        print(f"\nParsed Entry: {idx+1}")
        print("INPUT:", entry["input"])
        if "output" in entry:
            print("OUTPUT:", entry["output"])
        if "domain" in entry:
            print("DOMAIN:", entry["domain"])
        print()
    
    print("EOF or Max entries reached.")

if __name__ == "__main__":
    main()
