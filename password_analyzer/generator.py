import secrets
import string

def build_character_pool(
        use_lowercase: bool = True, 
        use_uppercase: bool = True,
        use_digits: bool = True,
        use_symbols: bool = True
) -> str:
    pool=""
    if use_lowercase:
        pool += string.ascii_lowercase

    if use_uppercase:
        pool += string.ascii_uppercase
    
    if use_symbols:
        pool += string.punctuation
    
    if use_digits:
        pool+= string.digits


    return pool

def generate_password(
        length: int = 16,
        use_lowercase: bool = True, 
        use_uppercase: bool = True, 
        use_digits: bool = True, 
        use_symbols: bool = True, 
) -> str:
    if length < 8:
        raise ValueError("Password length must be atleast 8 characters.")
    
    pool = build_character_pool(
        use_lowercase=use_lowercase,
        use_uppercase= use_uppercase,
        use_digits = use_digits,
        use_symbols = use_symbols,
    )

    if not pool:
        raise ValueError("At least one character set must be enabled.")
    
    return "".join(secrets.choice(pool) for _ in range(length))