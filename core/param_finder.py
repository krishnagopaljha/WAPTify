import requests
from urllib.parse import urlparse, parse_qs, urlunparse
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored
import re

def find_parameters(args):
    try:
        with open(args.wordlist) as f:
            parameters = [line.strip() for line in f if line.strip()]

        parsed_url = urlparse(args.url)
        base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))
        existing_query = parse_qs(parsed_url.query)
        
        print(colored(f"[*] Testing {len(parameters)} parameters on {args.url}", 'blue'))
        print(colored(f"[*] Methods: {', '.join(args.methods)} | Threads: {args.threads}\n", 'blue'))

        def test_param(param):
            found = []
            unique_value = f"paraMeterF1nd3r_{param}_t3s7v4lu3"  # Unique pattern for detection
            
            # Test GET method
            if 'GET' in args.methods:
                get_query = existing_query.copy()
                get_query[param] = unique_value
                try:
                    response = requests.get(
                        base_url,
                        params=get_query,
                        timeout=10,
                        allow_redirects=False
                    )
                    if re.search(re.escape(unique_value), response.text):
                        get_url = response.url
                        found.append(('GET', get_url))
                except:
                    pass
            
            # Test POST method
            if 'POST' in args.methods:
                post_query = existing_query.copy()
                post_data = {param: unique_value}
                try:
                    response = requests.post(
                        base_url,
                        params=post_query,
                        data=post_data,
                        timeout=10,
                        allow_redirects=False
                    )
                    if re.search(re.escape(unique_value), response.text):
                        post_url = f"{base_url}?{urlencode(post_query)}" if post_query else base_url
                        found.append(('POST', f"{post_url} (POST data: {param}={unique_value})"))
                except:
                    pass
            
            return found

        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            results = executor.map(test_param, parameters)

        found_params = []
        for result in results:
            if result:
                found_params.extend(result)

        if found_params:
            print(colored("\n[+] Discovered parameters:", 'green'))
            for method, url in found_params:
                print(colored(f"{method}: {url}", 'cyan'))
        else:
            print(colored("\n[-] No parameters found", 'red'))

    except Exception as e:
        print(colored(f"\n[!] Error: {str(e)}", 'red'))
