import string
import secrets
import math
import sys

NIST_MIN = 15
NIST_MAX = 64
APP_NAME = "DecodeLabs Enterprise Password Generator"
VERSION = "1.0.0"


def print_banner():
    banner = f"""
{'=' * 56}
  {APP_NAME}
  Version {VERSION} | NIST SP 800-63-4 Compliant
  Powered by cryptographically secure entropy (secrets)
{'=' * 56}"""
    print(banner)


def get_password_length():
    while True:
        try:
            raw = input(f"\nEnter desired password length [{NIST_MIN}-{NIST_MAX}]: ").strip()
            if not raw:
                print("  Input cannot be empty. Try again.")
                continue

            length = int(raw)

            if length <= 0:
                print("  Length must be a positive integer.")
                continue

            if length > NIST_MAX:
                print(f"  Capped at NIST maximum of {NIST_MAX} characters.")
                return NIST_MAX

            if length < NIST_MIN:
                print(f"\n  [WARNING] NIST SP 800-63-4 recommends a minimum of {NIST_MIN}")
                print(f"  characters for high-security contexts. You entered {length}.")
                confirm = input("  Proceed anyway? (y/n): ").strip().lower()
                if confirm == 'y':
                    return length
                continue

            return length

        except ValueError:
            print("  Invalid input. Please enter a whole number (e.g. 16).")


def get_character_preferences():
    print("\n  Character Set Configuration (press Enter to accept defaults):")

    def ask(prompt, default=True):
        suffix = "[Y/n]" if default else "[y/N]"
        raw = input(f"    {prompt} {suffix}: ").strip().lower()
        if raw == '':
            return default
        return raw == 'y'

    use_upper   = ask("Include UPPERCASE letters?")
    use_lower   = ask("Include lowercase letters?")
    use_digits  = ask("Include digits (0-9)?")
    use_symbols = ask("Include special characters (!@#$...)?")

    if not any([use_upper, use_lower, use_digits, use_symbols]):
        print("\n  [ERROR] You must select at least one character set.")
        print("  Defaulting to full alphanumeric set.\n")
        return True, True, True, False

    return use_upper, use_lower, use_digits, use_symbols


def build_character_pool(use_upper, use_lower, use_digits, use_symbols):
    pool = ""
    mandatory_chars = []

    if use_upper:
        pool += string.ascii_uppercase
        mandatory_chars.append(secrets.choice(string.ascii_uppercase))

    if use_lower:
        pool += string.ascii_lowercase
        mandatory_chars.append(secrets.choice(string.ascii_lowercase))

    if use_digits:
        pool += string.digits
        mandatory_chars.append(secrets.choice(string.digits))

    if use_symbols:
        pool += string.punctuation
        mandatory_chars.append(secrets.choice(string.punctuation))

    return pool, mandatory_chars


def generate_password(length, pool, mandatory_chars):
    remaining = length - len(mandatory_chars)

    if remaining < 0:
        password_list = [secrets.choice(pool) for _ in range(length)]
    else:
        filler = [secrets.choice(pool) for _ in range(remaining)]
        password_list = mandatory_chars + filler

    secrets.SystemRandom().shuffle(password_list)
    return ''.join(password_list)


def calculate_entropy(length, pool_size):
    if pool_size <= 1:
        return 0.0
    return length * math.log2(pool_size)


def get_strength_label(entropy_bits):
    if entropy_bits < 28:
        return "Very Weak",  "[!!]"
    elif entropy_bits < 50:
        return "Weak",       "[! ]"
    elif entropy_bits < 72:
        return "Reasonable", "[ok]"
    elif entropy_bits < 120:
        return "Strong",     "[**]"
    else:
        return "Very Strong","[##]"


def estimate_crack_time(entropy_bits, guesses_per_second=1_000_000_000):
    total_combinations = 2 ** entropy_bits
    seconds = total_combinations / guesses_per_second

    years = seconds / (60 * 60 * 24 * 365.25)

    if years < 1 / (365.25 * 24):
        return f"< 1 hour"
    elif years < 1:
        days = years * 365.25
        return f"~{days:.0f} day(s)"
    elif years < 1_000:
        return f"~{years:,.0f} year(s)"
    elif years < 1_000_000:
        return f"~{years / 1_000:,.1f} thousand years"
    elif years < 1_000_000_000:
        return f"~{years / 1_000_000:,.1f} million years"
    else:
        return "practically infinite"


def print_report(password, length, pool_size, entropy, strength_label, strength_icon, crack_time):
    print(f"""
{'=' * 56}
  GENERATED PASSWORD
{'=' * 56}
  {password}
{'─' * 56}
  Length       : {length} characters
  Character Pool: {pool_size} unique characters
  Entropy      : {entropy:.2f} bits
  Strength     : {strength_icon} {strength_label}
  Crack Time   : {crack_time}  (at 1B guesses/sec)
{'=' * 56}""")


def run_again_prompt():
    choice = input("\n  Generate another password? (y/n): ").strip().lower()
    return choice == 'y'


def main():
    print_banner()

    while True:
        length = get_password_length()
        use_upper, use_lower, use_digits, use_symbols = get_character_preferences()
        pool, mandatory_chars = build_character_pool(use_upper, use_lower, use_digits, use_symbols)

        password   = generate_password(length, pool, mandatory_chars)
        entropy    = calculate_entropy(length, len(pool))
        label, icon = get_strength_label(entropy)
        crack_time = estimate_crack_time(entropy)

        print_report(password, length, len(pool), entropy, label, icon, crack_time)

        if not run_again_prompt():
            print("\n  Session complete. Stay secure.\n")
            sys.exit(0)


if __name__ == "__main__":
    main()
