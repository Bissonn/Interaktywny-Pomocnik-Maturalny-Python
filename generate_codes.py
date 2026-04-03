#!/usr/bin/env python3
"""
generate_codes.py

Użycie:
  python generate_codes.py          # 1 kod, limit 3 użycia
  python generate_codes.py 5        # 5 kodów
  python generate_codes.py 1 5      # 1 kod, limit 5 użyć
"""
import json, secrets, string, sys, os
from datetime import date

CODES_FILE = os.path.join(os.path.dirname(__file__), "codes.json")

def gen_code():
    chars = string.ascii_uppercase + string.digits
    p1 = ''.join(secrets.choice(chars) for _ in range(4))
    p2 = ''.join(secrets.choice(chars) for _ in range(4))
    return f"MATURA-{p1}-{p2}"

def main():
    n        = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    max_uses = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    codes = json.load(open(CODES_FILE)) if os.path.exists(CODES_FILE) else {}

    new_codes = []
    for _ in range(n):
        code = gen_code()
        while code in codes:
            code = gen_code()
        codes[code] = {"uses": 0, "max_uses": max_uses, "created": str(date.today())}
        new_codes.append(code)

    with open(CODES_FILE, "w") as f:
        json.dump(codes, f, indent=2, ensure_ascii=False)

    print(f"\nWygenerowano {n} kod(y) [limit: {max_uses} uzytki]:\n")
    for c in new_codes:
        print(f"  {c}")
    print(f"\nWklej kod do szablonu maila w Naffy.")
    print(f"Kodow w bazie: {len(codes)}\n")

if __name__ == "__main__":
    main()
