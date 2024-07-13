import os
import json
import anthropic
import whois
import argparse
from dotenv import load_dotenv
from termcolor import colored

# Load environment variables
load_dotenv()

def generate_brand_names(theme, prefix=None, postfix=None, num_brands=100):
    client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )
    
    prompt = f"""You are tasked with creating a list of unique, innovative brand names based on the following parameters:

Theme: {theme}
Prefix (optional): {prefix if prefix else 'N/A'}
Postfix (optional): {postfix if postfix else 'N/A'}

Your goal is to generate brand names that have a timeless, iconic feeling, and aligning with the given theme.

Guidelines for creating brand names:
1. If a prefix is provided, start each name with it.
2. If a postfix is provided, end each name with it.
3. Create two types of brand names, based on one word (Word), or an adjective + one word (AdjectiveWord)
   a. Single-word names (e.g., PrefixWord, PrefixWordPostfix or WordPostfix)
   b. Two-word names (e.g., PrefixAdjectiveWord, PrefixAdjectiveWordPostfix, or AdjectiveWordPostfix)
4. Distribute the types equally: 50% single-word names and 50% two-word names

You will create a total of {num_brands} brand names.

For the Word, choose words that are evocative, cool, timeless, and interesting

For two-word names, the Adjective should complement the first and create a compelling combination.

Ensure that all brand names:
- Align with the provided theme
- Have an innovative feel
- Are unique and not repetitive
- Sound professional and marketable
- Are inspiring and evocative

Before you begin, take a moment to brainstorm a diverse range of words and combinations that fit these criteria and align with the given theme.

Once you have generated the list of brand names, output them in a JSON array format. Do not include any additional text, explanations, or numbering. The output should be a valid JSON array containing only the brand names as strings."""

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    
    return json.loads(message.content[0].text)

def read_existing_domains(filename):
    if not os.path.exists(filename):
        return set()
    with open(filename, 'r') as f:
        return set(line.strip().lower() for line in f if line.strip())

def check_domain_availability(domain):
    try:
        whois.whois(domain)
        return False
    except whois.parser.PywhoisError:
        return True

def main(theme, prefix=None, postfix=None, num_brands=100):
    available_file = "available_domains.txt"
    unavailable_file = "unavailable_domains.txt"
    
    # Generate brand names
    brand_names = generate_brand_names(theme, prefix, postfix, num_brands)
    
    # Read existing domains
    existing_available = read_existing_domains(available_file)
    existing_unavailable = read_existing_domains(unavailable_file)
    
    # Exclude already checked domains
    brand_names = [name for name in brand_names if name.lower() + ".com" not in existing_available and name.lower() + ".com" not in existing_unavailable]
    print(f"Excluding {num_brands - len(brand_names)} domains already checked.")
    print(f"Excluding {len(existing_unavailable)} unavailable domains already checked.")
    
    # Check domain availability
    available_domains = []
    unavailable_domains = []
    for name in brand_names:
        domain = f"{name}.com"
        print(f"Checking {domain}...", end=" ")
        if check_domain_availability(domain):
            print(colored("AVAILABLE", "green"))
            available_domains.append(domain)
        else:
            print(colored("TAKEN", "red"))
            unavailable_domains.append(domain)
    
    # Write results to files
    with open(available_file, 'a') as f:
        for domain in available_domains:
            f.write(f"{domain}\n")
    
    with open(unavailable_file, 'a') as f:
        for domain in unavailable_domains:
            f.write(f"{domain}\n")
    
    print(f"\nAvailable domains have been added to {available_file}")
    print(f"Unavailable domains have been added to {unavailable_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate and check availability of domain names based on a theme.")
    parser.add_argument("theme", help="General theme for the kind of website you're trying to name")
    parser.add_argument("--prefix", help="Word to use as a prefix for the domain names")
    parser.add_argument("--postfix", help="Word to use as a postfix for the domain names")
    parser.add_argument("--num_brands", type=int, default=100, help="Number of brand names to generate")
    
    args = parser.parse_args()
    
    main(args.theme, args.prefix, args.postfix, args.num_brands)