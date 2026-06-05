import argparse
import getpass
import json

from password_analyzer.analyzer import analyze_password
from password_analyzer.breaches import check_password_against_hash_file
from password_analyzer.generator import generate_password


def print_human_report(result: dict) -> None:
    print("\nPassword Analysis")
    print("-----------------")
    print(f"Length: {result['length']}")
    print(f"Character pool size: {result['character_pool_size']}")
    print(f"Character sets used: {', '.join(result['character_sets']) or 'none'}")
    print(f"Entropy: {result['entropy_bits']} bits")
    print(f"Estimated crack time: {result['estimated_crack_time']}")

    if "breach_check" in result:
        breach_check = result["breach_check"]
        status = "FOUND" if breach_check["breached"] else "not found"
        print(f"Breach check: {status} in {breach_check['hashes_checked']} hashes")

    print("\nRecommendations")
    print("---------------")
    for recommendation in result["recommendations"]:
        print(f"- {recommendation}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="password-analyzer",
        description="Evaluate password strength using NIST-inspired checks.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze one password.",
    )
    analyze_parser.add_argument(
        "password",
        nargs="?",
        help="Password to analyze. If omitted, you will be prompted securely.",
    )
    analyze_parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON output.",
    )
    analyze_parser.add_argument(
        "--breach-hashes",
        metavar="PATH",
        help="Path to a file containing SHA-1 password hashes.",
    )
    generate_parser = subparsers.add_parser(
        "generate",
        help= "Generate a strong password.",
    )

    generate_parser.add_argument(
        "--length",
        type=int,
        default= 16,
        help="Password length. Default: 16."
    )

    generate_parser.add_argument(
        "--no-lowercase",
        action ="store_true",
        help="Exclude lowercase letters",
    )

    generate_parser.add_argument(
        "--no-uppercase",
        action ="store_true",
        help="Exclude uppercase letters."
    )

    generate_parser.add_argument(
        "--no-digits",
        action="store_true",
        help="Exclude digits."
    )

    generate_parser.add_argument(
        "--no-symbols",
        action="store_true",
        help="Exclude symbols."
    )


    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "analyze":
        password = args.password or getpass.getpass("Password: ")
        result = analyze_password(password)

        if args.breach_hashes:
            result["breach_check"] = check_password_against_hash_file(
                password,
                args.breach_hashes,
            )
            if result["breach_check"]["breached"]:
                result["recommendations"].insert(
                    0,
                    "Do not use this password. It appears in a known breach list.",
                )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print_human_report(result)
    
    elif args.command == "generate":
        password = generate_password(
            length=args.length,
            use_lowercase = not args.no_lowercase,
            use_uppercase = not args.no_uppercase,
            use_digits= not args.no_digits,
            use_symbols = not args.no_symbols,
        )
        print(password)


if __name__ == "__main__":
    main()
