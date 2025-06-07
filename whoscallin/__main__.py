import argparse
import sys
from whoscallin import WhosCallin
from whoscallin.schemas import CallerInfo

TOKEN_FILE = "trucaller.token"

def do_login(args):
    phone = args.phone
    country = args.country
    verbose = args.verbose
    wc = WhosCallin.login(phone, countryCode=country, verbose=verbose)
    wc.saveToken(TOKEN_FILE)
    print("Login successful! Token saved.")

def do_info(args):
    token = None
    if args.token:
        token = args.token
        wc = WhosCallin(token)
    else:
        try:
            wc = WhosCallin.loadToken(TOKEN_FILE)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    info = wc.callerInfo(args.phone, countryCode=args.country)
    if args.export:
        with open(args.export, 'w') as f:
            f.write(info.model_dump_json(indent=2))
        print(f"Caller info exported to {args.export}")
        return
    if args.json:
        print(info.model_dump_json(indent=2))
        return
    print_caller_info(info, verbose=args.verbose)

def do_token(args):
    if args.set:
        wc = WhosCallin(args.set)
        wc.saveToken(TOKEN_FILE)
        print("Token saved.")
    else:
        try:
            wc = WhosCallin.loadToken(TOKEN_FILE)
            print(wc.token)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

def print_caller_info(info: CallerInfo, verbose:bool = False):
    if verbose:
        print("\n" + "="*40)
        print("Verbose")
    print("\n" + "="*40)
    print(f"\nCaller Info for {info.name} (ID: {info.id})")
    print(f"Score: {info.score}\nPhones:")
    for p in info.phones:
        print(f" - {p.e164Format} ({p.type})")
    print(f"Addresses: {len(info.addresses)} found.")
    print(f"Tags: {', '.join(info.tags) if info.tags else 'None'}")
    print(f"Badges: {', '.join(info.badges) if info.badges else 'None'}")
    print(f"Access: {info.access}")
    print(f"Enhanced: {'Yes' if info.enhanced else 'No'}")
    # Internet addresses
    for iaddr in info.internetAddresses:
        print("Internet Address: ")
        print(f"- {iaddr.get('caption')}")
        print(f"\t- {iaddr.get('service')}: {iaddr.get('id')}")
    
    if verbose: print(info.model_dump())

    print("\n" + "="*40)

def main():
    parser = argparse.ArgumentParser(description="WhosCallin CLI - Lookup caller info using the Truecaller API (unofficial).")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Login command
    login_parser = subparsers.add_parser("login", help="Login and save token")
    login_parser.add_argument("phone", help="Your phone number (E.164 format, e.g., 911234567890)")
    login_parser.add_argument("--country", default="in", help="Country code (default: in)")
    login_parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    login_parser.set_defaults(func=do_login)

    # Info command
    info_parser = subparsers.add_parser("info", help="Lookup caller info by phone number")
    info_parser.add_argument("phone", help="Phone number to lookup (E.164 format, e.g., 911234567890)")
    info_parser.add_argument("--token", help="Truecaller API token (if not using saved token)")
    info_parser.add_argument("--country", default="in", help="Country code (default: in)")
    info_parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    info_parser.add_argument("-j", "--json", action="store_true", help="Output in JSON format to stdout")
    info_parser.add_argument("-e", "--export", help="Export caller info to a file (JSON format)")
    info_parser.set_defaults(func=do_info)

    # Token command
    token_parser = subparsers.add_parser("token", help="Show or set the saved token")
    token_parser.add_argument("--set", help="Set and save a token")
    token_parser.set_defaults(func=do_token)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
