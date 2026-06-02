# DecodeLabs — Project 3: Enterprise Random Password Generator

> **NIST SP 800-63-4 Compliant** · Built with Python stdlib only · Zero external dependencies

---

## Overview

A command-line password generator that implements enterprise-grade security
standards. Goes beyond the basic requirement of "letters and numbers" by using
cryptographically secure randomness, enforcing NIST 2024 length guidelines,
guaranteeing character-type coverage, and providing real-time entropy analysis.

---

## Features

| Feature | Junior Approach | This Project |
|---|---|---|
| Randomness | `random.choice()` (Mersenne Twister) | `secrets.choice()` (OS entropy) |
| String building | `password += char` — O(N²) | `''.join(list)` — O(N) |
| Character sets | Hardcoded strings | `string` module constants |
| Input validation | None | Full type + range checking |
| Security metric | None | Shannon entropy (bits) |
| Crack time estimate | None | GPU-speed brute-force model |

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/<your-username>/password-generator.git
cd password-generator

# Run (no install needed — pure stdlib)
python password_generator.py
```

### Sample Session

```
========================================================
  DecodeLabs Enterprise Password Generator
  Version 1.0.0 | NIST SP 800-63-4 Compliant
  Powered by cryptographically secure entropy (secrets)
========================================================

Enter desired password length [15-64]: 20

  Character Set Configuration (press Enter to accept defaults):
    Include UPPERCASE letters? [Y/n]:
    Include lowercase letters? [Y/n]:
    Include digits (0-9)? [Y/n]:
    Include special characters (!@#$...)? [Y/n]:

========================================================
  GENERATED PASSWORD
========================================================
  gT#9xL$mQp2!Rn@wZk7
────────────────────────────────────────────────────────
  Length        : 20 characters
  Character Pool: 94 unique characters
  Entropy       : 131.10 bits
  Strength      : [##] Very Strong
  Crack Time    : practically infinite  (at 1B guesses/sec)
========================================================
```

---

## Project Structure

```
password-generator/
├── password_generator.py      # Main application
├── tests/
│   └── test_password_generator.py   # Unit test suite (17 tests)
├── .gitignore
└── README.md
```

---

## Key Concepts Demonstrated

### 1. `secrets` vs `random`
`random` uses the Mersenne Twister — a deterministic algorithm seeded by system
time. An attacker who knows the seed can reproduce every "random" choice.
`secrets` pulls from the OS's hardware entropy pool, making outputs
mathematically unpredictable.

### 2. Shannon Entropy Formula
```
E = L × log₂(R)
```
- **E** = entropy in bits (higher = more secure)
- **L** = password length
- **R** = size of character pool (e.g., 94 for full ASCII printable)

A password with 128+ bits of entropy is considered unbreakable by brute force
with current and near-future computing hardware.

### 3. O(N) String Assembly
Strings in Python are immutable. Concatenating with `+=` inside a loop creates
a new object on every iteration — O(N²) memory. Building a list and calling
`''.join()` at the end performs a single allocation — O(N).

---

## Running Tests

```bash
python -m unittest tests/test_password_generator.py -v
```

Expected output: **17 tests, 0 failures.**

---

## NIST SP 800-63-4 Compliance

| Requirement | Implementation |
|---|---|
| Minimum 15 characters for high-security | Enforced with user warning |
| Maximum 64 characters | Hard cap applied |
| No mandatory complexity rules | User chooses character sets |
| No periodic forced resets | Stateless tool — generates on demand |

---

## Author

**Prasanna Chidambar Marihalkar**  
First-Year CSE · PES University, RR Campus · DecodeLabs Batch 2026
