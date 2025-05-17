import argparse
from core.jwt_tool import jwt_encode_decode
from core.param_finder import find_parameters
from core.lfi_tester import test_lfi
from core.xss_checker import check_xss
from core.redirect_checker import check_open_redirect
from core.dir_bruteforcer import bruteforce_directories

def main():
    # Main parser setup
    parser = argparse.ArgumentParser(
        description="Web Application Penetration Testing Toolkit (WAPT)",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""\033[1;36m
Examples:
  Basic Scans:
    main.py param -u https://example.com -w params.txt
    main.py dir -u https://example.com -w common_dirs.txt

  Vulnerability Testing:
    main.py xss -u https://example.com/search -p query -w xss_payloads.txt
    main.py lfi -u http://vuln.site/view?file= -p file

  JWT Operations:
    main.py jwt --encode --payload-file data.json --secret mykey
    main.py jwt --decode --token-file auth.jwt --secret mykey

  Open Redirect Check:
    main.py redirect -u https://example.com/redirect -p url

\033[1;33m
Note: Always get proper authorization before testing any systems.
For detailed command help: main.py <command> -h\033[0m
        """
    )
    
    subparsers = parser.add_subparsers(
        title="Available Commands",
        dest='command',
        metavar="<command>",
        required=True
    )

    # JWT Tool Help
    jwt_help = """\033[1mJWT Encoding/Decoding Operations\033[0m

Encode/Decode JSON Web Tokens with HS256 algorithm

\033[1mExamples:\033[0m
  Encode from file:   main.py jwt --encode --payload-file data.json --secret mykey
  Decode from CLI:    main.py jwt --decode --token "eyJ..." --secret mykey
  Save to file:       main.py jwt --encode --payload '{"user":"admin"}' -o token.jwt

\033[1mArguments:\033[0m"""
    jwt_parser = subparsers.add_parser('jwt', 
                                     help='JWT operations',
                                     description=jwt_help,
                                     formatter_class=argparse.RawTextHelpFormatter)
    # ... (rest of jwt arguments from previous implementation)

    # Parameter Finder Help
    param_help = """\033[1mHidden Parameter Discovery\033[0m

Discover hidden parameters using fuzzing techniques

\033[1mExamples:\033[0m
  Basic scan:         main.py param -u https://example.com -w params.txt
  Multi-threaded:     main.py param -u https://api.example.com -w params.txt -t 20
  POST method only:   main.py param -u https://example.com/login -w params.txt -m POST

\033[1mArguments:\033[0m"""
    param_parser = subparsers.add_parser('param', 
                                       help='Parameter discovery',
                                       description=param_help,
                                       formatter_class=argparse.RawTextHelpFormatter)
    # ... (rest of param arguments from previous implementation)

    # LFI Tester Help
    lfi_help = """\033[1mLocal File Inclusion Tester\033[0m

Test for file inclusion vulnerabilities

\033[1mExamples:\033[0m
  Basic test:         main.py lfi -u http://vuln.site/view?file= -p file
  POST request:       main.py lfi -u http://vuln.site/load -p document -m POST

\033[1mArguments:\033[0m"""
    lfi_parser = subparsers.add_parser('lfi', 
                                     help='LFI testing',
                                     description=lfi_help,
                                     formatter_class=argparse.RawTextHelpFormatter)
    # ... (rest of lfi arguments)

    # XSS Checker Help
    xss_help = """\033[1mXSS Vulnerability Scanner\033[0m

Test for Cross-Site Scripting vulnerabilities

\033[1mExamples:\033[0m
  Default payloads:   main.py xss -u https://example.com/search -p query
  Custom payloads:    main.py xss -u https://example.com/comment -p text -w xss_payloads.txt
  POST method:        main.py xss -u https://example.com/login -p username,email -m POST

\033[1mArguments:\033[0m"""
    xss_parser = subparsers.add_parser('xss', 
                                     help='XSS detection',
                                     description=xss_help,
                                     formatter_class=argparse.RawTextHelpFormatter)
    # ... (rest of xss arguments)

    # Redirect Checker Help
    redirect_help = """\033[1mOpen Redirect Detector\033[0m

Check for open redirect vulnerabilities

\033[1mExamples:\033[0m
  Basic check:        main.py redirect -u https://example.com/redirect -p url
  Full test:          main.py redirect -u https://auth.example.com/callback -p returnUrl

\033[1mArguments:\033[0m"""
    redirect_parser = subparsers.add_parser('redirect', 
                                          help='Open redirect detection',
                                          description=redirect_help,
                                          formatter_class=argparse.RawTextHelpFormatter)
    # ... (rest of redirect arguments)

    # Directory Bruteforcer Help
    dir_help = """\033[1mDirectory Bruteforcer\033[0m

Discover hidden directories and files

\033[1mExamples:\033[0m
  Common dirs:        main.py dir -u https://example.com -w common_dirs.txt
  High concurrency:   main.py dir -u https://api.example.com -w big_list.txt -t 50

\033[1mArguments:\033[0m"""
    dir_parser = subparsers.add_parser('dir', 
                                    help='Directory bruteforcing',
                                    description=dir_help,
                                    formatter_class=argparse.RawTextHelpFormatter)
    # ... (rest of dir arguments)

    # Parse arguments and execute
    args = parser.parse_args()
    
    # ... (rest of execution logic from previous implementation)

if __name__ == '__main__':
    main()
