# Domain Finder

Domain Finder is a Python script that generates brand names based on a given theme and checks their availability as domain names.

I made this because I was sick of having to think of company names and then check individual availability of .com domains.

## Features

- Generate brand names using the Anthropic API
- Check domain availability
- Customizable with optional prefix and postfix
- Outputs lists of available and unavailable domain names

## Installation

1. Ensure you have Python installed on your system.
2. Clone this repository:
   ```
   git clone https://github.com/yourusername/domain-finder.git
   cd domain-finder
   ```
3. Install the required libraries:
   ```
   pip install anthropic whois python-dotenv termcolor
   ```
4. Set up an Anthropic API key and add it to a `.env` file in the project root:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Usage

Run the script from the command line:

```
python domain_finder.py "your theme" --prefix optional_prefix --postfix optional_postfix --num_brands 100
```

## File Structure

```
domainFinder/
├── domain_finder.py         # Main script for generating and checking domains
├── available_domains.txt    # List of available domain names
└── unavailable.txt          # List of unavailable domain names
```

## How It Works

1. The script generates brand names based on the given theme using the Anthropic API.
2. It then checks the availability of each generated domain name.
3. Available and unavailable domain names are written to separate text files.

## Functions

- `generate_brand_names(theme, prefix=None, postfix=None, num_brands=100)`: Generates brand names using the Anthropic API.
- `read_existing_domains(filename)`: Reads existing domain names from a file to avoid rechecking.
- `check_domain_availability(domain)`: Checks if a given domain is available for registration.
- `main(theme, prefix=None, postfix=None, num_brands=100)`: Orchestrates the entire process.

## Potential Improvements

- Implement rate limiting handling for API calls
- Enhance error handling
- Optimize performance with parallel processing
- Develop a graphical user interface
- Implement additional domain name validation
- Use a database for better data management
- Add more customization options for brand name generation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT public license