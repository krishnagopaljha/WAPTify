import requests
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored

def check_directory(url, directory):
    try:
        target = f"{url}/{directory}"
        response = requests.get(target)
        if response.status_code == 200:
            print(colored(f"[+] Found directory: /{directory}", 'green'))
    except:
        pass

def bruteforce_directories(args):
    try:
        with open(args.wordlist) as f:
            directories = f.read().splitlines()
        
        print(colored(f"[*] Bruteforcing directories on {args.url}", 'blue'))
        
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            for directory in directories:
                executor.submit(check_directory, args.url, directory)
                
    except Exception as e:
        print(colored(f"Error bruteforcing directories: {str(e)}", 'red'))
