import requests
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored
import re

def get_wayback_params(domain):
    """Fetch parameters from Wayback Machine archives"""
    params = set()
    try:
        response = requests.get(
            "http://web.archive.org/cdx/search/cdx",
            params={
                'url': f'*.{domain}/*',
                'output': 'text',
                'fl': 'original',
                'collapse': 'urlkey'
            },
            timeout=15
        )
        if response.status_code == 200:
            for url in response.text.splitlines():
                try:
                    parsed = urlparse(url)
                    query = parse_qs(parsed.query)
                    params.update(query.keys())
                except:
                    continue
    except:
        pass
    return params

def find_parameters(args):
    try:
        parsed_url = urlparse(args.url)
        domain = parsed_url.hostname
        if not domain:
            print(colored("[!] Invalid URL format", 'red'))
            return

        # Get parameters from wordlist and Wayback Machine
        with open(args.wordlist) as f:
            wordlist_params = [line.strip() for line in f if line.strip()]
        
        wayback_params = get_wayback_params(domain)
        
        # Merge parameters with deduplication
        seen = set()
        parameters = []
        for p in wordlist_params + list(wayback_params):
            if p not in seen and p:
                seen.add(p)
                parameters.append(p)

        base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))
        existing_query = parse_qs(parsed_url.query)
        
        print(colored(f"[*] Testing {len(parameters)} parameters on {args.url}", 'blue'))
        print(colored(f"[*] Methods: {', '.join(args.methods)} | Threads: {args.threads}\n", 'blue'))

        found_params = []
        unique_value = "paraMeterF1nd3r_%s_t3s7v4lu3"  # Pattern with placeholder

        def test_param(param):
            local_found = []
            current_value = unique_value % param  # Unique value per parameter
            
            # Test GET method
            if 'GET' in args.methods:
                get_query = existing_query.copy()
                get_query[param] = current_value
                try:
                    response = requests.get(
                        base_url,
                        params=get_query,
                        timeout=10,
                        allow_redirects=False
                    )
                    if re.search(re.escape(current_value), response.text):
                        local_found.append(('GET', response.url))
                except:
                    pass
            
            # Test POST method
            if 'POST' in args.methods:
                post_query = existing_query.copy()
                post_data = {param: current_value}
                try:
                    response = requests.post(
                        base_url,
                        params=post_query,
                        data=post_data,
                        timeout=10,
                        allow_redirects=False
                    )
                    if re.search(re.escape(current_value), response.text):
                        post_url = f"{base_url}?{urlencode(post_query)}" if post_query else base_url
                        local_found.append(('POST', f"{post_url} (POST data: {param}={current_value})"))
                except:
                    pass
            
            return local_found

        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            results = executor.map(test_param, parameters)

        for result in results:
            if result:
                found_params.extend(result)

        # Save results to file
        if found_params:
            filename = f"{domain}.txt"
            with open(filename, 'w') as f:
                for method, url in found_params:
                    f.write(f"{method}: {url}\n")
            
            print(colored("\n[+] Discovered parameters:", 'green'))
            for method, url in found_params:
                print(colored(f"{method}: {url}", 'cyan'))
            print(colored(f"\n[+] Results saved to {filename}", 'green'))
        else:
            print(colored("\n[-] No parameters found", 'red'))

    except Exception as e:
        print(colored(f"\n[!] Error: {str(e)}", 'red'))
