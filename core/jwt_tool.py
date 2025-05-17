import jwt
import json
from termcolor import colored
import os

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(colored(f"Error reading JSON file: {str(e)}", 'red'))
        return None

def read_token_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return f.read().strip()
    except Exception as e:
        print(colored(f"Error reading token file: {str(e)}", 'red'))
        return None

def save_result(content, output_file):
    try:
        with open(output_file, 'w') as f:
            f.write(content)
        print(colored(f"\nResults saved to: {os.path.abspath(output_file)}", 'cyan'))
    except Exception as e:
        print(colored(f"Error saving file: {str(e)}", 'red'))

def jwt_encode_decode(args):
    result = None
    
    if args.encode:
        # Handle payload input
        payload = None
        if args.payload_file:
            payload = read_json_file(args.payload_file)
        elif args.payload:
            try:
                payload = json.loads(args.payload)
            except json.JSONDecodeError:
                print(colored("Invalid JSON payload string", 'red'))
                return
        
        if payload:
            try:
                token = jwt.encode(payload, args.secret or '', algorithm='HS256')
                result = f"Encoded JWT:\n{token}"
                print(colored(result, 'green'))
            except Exception as e:
                print(colored(f"Error encoding JWT: {str(e)}", 'red'))
    
    elif args.decode:
        # Handle token input
        token = None
        if args.token_file:
            token = read_token_file(args.token_file)
        elif args.token:
            token = args.token
        
        if token:
            try:
                decoded = jwt.decode(token, args.secret or '', algorithms=['HS256'])
                result = "Decoded JWT:\n" + json.dumps(decoded, indent=2)
                print(colored(result, 'green'))
            except Exception as e:
                print(colored(f"Error decoding JWT: {str(e)}", 'red'))
    
    # Save results to file if requested
    if args.output and result:
        save_result(result, args.output)
