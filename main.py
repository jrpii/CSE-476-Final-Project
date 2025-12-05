### Main script, will eventually be entry point for agent loop.
import sys
import argparse
import random
from src.utils import parse_json_input, truncate, normalize_answer
from src.agent import call_agent
from src.prompts import get_system_prompt, get_extract_prompt

# Address Unicode encoding for Windows (keep parsed data unchanged.)
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="Path to JSON file for agent to parse.")
    parser.add_argument("--max-entries", type=int, default=None, help="Max entries to process.")
    parser.add_argument("--max-reasoning-tokens", type=int, default=512, help="Max tokens for reasoning pass.")
    parser.add_argument("--max-answer-tokens", type=int, default=128, help="Max tokens for answer extraction pass.")
    
    args = parser.parse_args()
    
    data = parse_json_input(args.input)

    # Sort by domain, then randomly sample up to max-entries per domain (when domain is available, else do max overall).
    if args.max_entries is not None:
        with_domain = []
        without_domain = []
        for item in data:
            if "domain" in item and item["domain"] is not None:
                with_domain.append(item)
            else:
                without_domain.append(item)

        if with_domain:
            by_domain = {}
            for item in with_domain:
                domain = item.get("domain")
                by_domain.setdefault(domain, []).append(item)

            sampled = []
            for domain, entries in by_domain.items():
                if len(entries) > args.max_entries:
                    sampled.extend(random.sample(entries, args.max_entries))
                else:
                    sampled.extend(entries)

            data = sampled
            random.shuffle(data)
        else:
            data = without_domain[:args.max_entries]
    
    print(f"Loaded {len(data)} entries.\n", flush=True)
    
    # Correctness tracking for dev.
    total_answered = 0
    total_correct = 0
    domain_stats = {}
    
    # Simple two-pass inference loop
    for idx, entry in enumerate(data, 1):
        print(f"\nEntry {idx}/{len(data)}", flush=True)
        print(f"INPUT: {truncate(entry['input'], 500)}", flush=True)
        
        # Get system prompt based on domain (seperated in order to add domain approximation later to handle test data).
        domain = entry.get("domain", "unknown")
        system_prompt = get_system_prompt(domain)
        
        # Reasoning call
        reasoning = call_agent(
            system_prompt=system_prompt,
            user_message=entry["input"],
            max_tokens=args.max_reasoning_tokens
        )
        
        final_answer = None

        # If no error, print reasoning and then extract the answer.
        if reasoning["ok"]:
            print(f"REASONING OUTPUT:\n{reasoning['text']}", flush=True)

            # Extraction call
            extract_system = get_extract_prompt(domain)
            extract_user = (
                "Problem:\n"
                f"{entry['input']}\n"
                "Draft solution:\n"
                f"{reasoning['text']}\n"
                "Extract and return only the final answer string."
            )
            extraction = call_agent(
                system_prompt=extract_system,
                user_message=extract_user,
                max_tokens=args.max_answer_tokens
            )

            if extraction["ok"] and extraction["text"] is not None:
                model_answer = extraction["text"].strip()
                final_answer = normalize_answer(model_answer)
                print(f"FINAL ANSWER: {final_answer}", flush=True)
            else:
                print(f"ERROR (extraction): {extraction['error']}", flush=True)
        else:
            print(f"ERROR (reasoning): {reasoning['error']}", flush=True)

        if "output" in entry and final_answer is not None:
            # Track global and per-domain stats (correct, total)
            total_answered += 1
            is_correct = (final_answer == entry["output"])
            if is_correct:
                total_correct += 1
            if domain not in domain_stats:
                domain_stats[domain] = [0, 0]
            domain_stats[domain][1] += 1
            if is_correct:
                domain_stats[domain][0] += 1

            print(f"EXPECTED ANSWER: {entry['output']}", flush=True)
            status = "CORRECT :)" if is_correct else "INCORRECT :("
            print(f"RESULT: {status}", flush=True)
    
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
