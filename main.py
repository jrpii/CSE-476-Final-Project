### Main script, will eventually be entry point for agent loop.
import sys
import argparse
from src.utils import parse_json_input, truncate
from src.agent import call_agent
from src.prompts import get_system_prompt

# Address Unicode encoding for Windows (keep parsed data unchanged.)
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Path to JSON file for agent to parse.")
    parser.add_argument("--max", type=int, default=None, help="Max entries to process.")
    parser.add_argument("--max-tokens", type=int, default=512, help="Max tokens for agent response.")
    
    args = parser.parse_args()
    
    data = parse_json_input(args.input)
    
    # Truncate data to max entries (parser still process whole file).
    if args.max is not None:
        data = data[:args.max]
    
    print(f"Loaded {len(data)} entries.\n", flush=True)
    
    # Correctness tracking for dev.
    total_answered = 0
    total_correct = 0
    domain_stats = {}
    
    # Simple inference loop
    for idx, entry in enumerate(data, 1):
        print(f"\nEntry {idx}/{len(data)}", flush=True)
        print(f"INPUT: {truncate(entry['input'], 500)}", flush=True)
        
        # Get system prompt based on domain (seperated in order to add domain approximation later to handle test data).
        domain = entry.get("domain", "unknown")
        system_prompt = get_system_prompt(domain)
        
        # Simple agent call
        result = call_agent(
            system_prompt=system_prompt,
            user_message=entry["input"],
            max_tokens=args.max_tokens
        )
        
        # If no error, print output and ground truth (if available).
        if result["ok"]:
            print(f"AGENT OUTPUT: {result['text']}", flush=True)
            if "output" in entry:
                # Track global and per-domain stats (correct, total)
                total_answered += 1
                is_correct = (result['text'] == entry['output'])
                if is_correct:
                    total_correct += 1
                if domain not in domain_stats:
                    domain_stats[domain] = [0, 0]
                domain_stats[domain][1] += 1
                if is_correct:
                    domain_stats[domain][0] += 1
                
                print(f"EXPECTED ANSWER: {entry['output']}", flush=True)
                print(f"RESULT: {"CORRECT :)" if is_correct else "INCORRECT :("}", flush=True)
        else:
            print(f"ERROR: {result['error']}", flush=True)
    
    # Final correct tallys.
    print("\nFinal Correct Tallys:", flush=True)
    if total_answered > 0:
        print(f"Overall: {total_correct}/{total_answered} correct ({(total_correct / total_answered) * 100:.2f}%)", flush=True)
    
    if domain_stats:
        print(f"\nPer-Domain Statistics:", flush=True)
        for domain, (correct, total) in sorted(domain_stats.items()):
            domain_pct = (correct / total) * 100 if total > 0 else 0.0
            print(f"  {domain}: {correct}/{total} correct ({domain_pct:.2f}%)", flush=True)
    
    print(f"\nAll entries processed... Exiting!\n", flush=True)

if __name__ == "__main__":
    main()
