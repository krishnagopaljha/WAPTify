import requests
from urllib.parse import urlparse
from termcolor import colored

def check_open_redirect(args):
    test_url = "https://google.com"
    try:
        parsed = urlparse(args.url)
        target = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        
        response = requests.get(target, params={args.param: test_url}, allow_redirects=False)
        
        if 300 <= response.status_code < 400:
            location = response.headers.get('Location', '')
            if urlparse(location).netloc == urlparse(test_url).netloc:
                print(colored(f"[+] Open redirect vulnerability found in parameter: {args.param}", 'green'))
                return
        print(colored("[-] No open redirect vulnerability found", 'red'))
    except Exception as e:
        print(colored(f"Error checking redirect: {str(e)}", 'red'))
