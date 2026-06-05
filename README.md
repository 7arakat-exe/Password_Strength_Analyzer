# Password Strength Analyzer

A Python CLI tool that evaluates password strength using NIST-inspired guidance, estimates entropy and crack time, checks passwords against breach-list hash files, and generates strong passwords using cryptographically secure randomness.

## Features

- Analyze password length and character diversity
- Estimate password entropy
- Estimate approximate crack time
- Provide NIST SP 800-63B inspired recommendations
- Check passwords against SHA-1 breach hash lists
- Generate strong random passwords
- Use a command-line interface built with `argparse`
- Include unit tests

## Project Structure

```text
Password_Strength_Analyzer/
  password_analyzer/
    analyzer.py
    breaches.py
    cli.py
    generator.py
    __init__.py
    tests/
      test_analyzer.py
      fixtures/
        breached_sha1.txt
  requirements.txt
  README.md
```

## Usage

Run commands from the project root.

### Analyze a Password

```bash
python -m password_analyzer.cli analyze "correcthorsebatterystaple"
```

If you omit the password, the tool will prompt you securely:

```bash
python -m password_analyzer.cli analyze
```

### JSON Output

```bash
python -m password_analyzer.cli analyze "P@ssw0rd123" --json
```

### Check Against a Breach Hash File

The breach checker compares the SHA-1 hash of the password against a file of known breached SHA-1 hashes.

```bash
python -m password_analyzer.cli analyze password --breach-hashes password_analyzer\tests\fixtures\breached_sha1.txt
```

The tool supports hash files formatted like this:

```text
5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8
```

or like this:

```text
5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8:3303003
```

### Generate a Strong Password

```bash
python -m password_analyzer.cli generate
```

Generate a longer password:

```bash
python -m password_analyzer.cli generate --length 24
```

Exclude symbols:

```bash
python -m password_analyzer.cli generate --length 20 --no-symbols
```

## Testing

Run the unit tests with:

```bash
python -m unittest password_analyzer.tests.test_analyzer
```

## Security Notes

This tool is for educational and portfolio purposes.

- The tool does not store analyzed passwords.
- Breach checks should use hashes instead of raw password lists.
- SHA-1 is used only for breach-list lookup compatibility.
- SHA-1 should not be used to store passwords in real applications.
- Real applications should use password hashing algorithms such as Argon2, bcrypt, or scrypt.
- Do not commit large raw breach datasets such as `rockyou.txt`.

## NIST-Inspired Guidance

This project follows several ideas inspired by NIST SP 800-63B:

- Encourage longer passwords
- Avoid relying only on composition rules
- Check passwords against known compromised password lists
- Provide practical recommendations instead of arbitrary complexity scoring

## Skills Demonstrated

- Python
- CLI development
- `argparse`
- Secure random generation with `secrets`
- Hashing with `hashlib`
- Unit testing
- Basic security engineering concepts
