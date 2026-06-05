import hashlib
from pathlib import Path


def sha1_password(password: str) -> str:
    return hashlib.sha1(password.encode("utf-8")).hexdigest().upper()


def normalize_hash_line(line: str) -> str | None:
    candidate = line.strip().upper()

    if not candidate:
        return None

    # Supports both plain SHA-1 hash files and HASH:COUNT formats.
    candidate = candidate.split(":", 1)[0]

    if len(candidate) != 40:
        return None

    try:
        int(candidate, 16)
    except ValueError:
        return None

    return candidate


def load_breach_hashes(hash_file: str | Path) -> set[str]:
    hashes = set()

    with Path(hash_file).open("r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            password_hash = normalize_hash_line(line)
            if password_hash is not None:
                hashes.add(password_hash)

    return hashes


def check_password_against_hashes(password: str, hashes: set[str]) -> bool:
    return sha1_password(password) in hashes


def check_password_against_hash_file(password: str, hash_file: str | Path) -> dict:
    hashes = load_breach_hashes(hash_file)

    return {
        "breached": check_password_against_hashes(password, hashes),
        "hashes_checked": len(hashes),
    }
