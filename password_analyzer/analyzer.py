import math
import string

def get_character_pool(password: str) -> tuple[int, list[str]]:
    pool_size = 0
    sets_used = []

    if any(c in string.ascii_lowercase for c in password):
        pool_size += 26
        sets_used.append("lowercase")
    
    if any(c in string.ascii_uppercase for c in password):
        pool_size += 26
        sets_used.append("uppercase")
    
    if any(c in string.digits for c in password):
        pool_size += 10
        sets_used.append("digits")

    if any(c in string.punctuation for c in password):
        pool_size += len(string.punctuation)
        sets_used.append("symbols")

    return pool_size, sets_used

def calculate_entropy(password: str) -> float:
    pool_size, _ = get_character_pool(password)

    if not password or pool_size == 0:
        return 0.0
    
    return len(password) * math.log2(pool_size)

def estimate_crack_time(entropy_bits: float, guesses_per_second: int = 1_000_000_000) -> str:
    guesses = 2 ** entropy_bits
    seconds = guesses / guesses_per_second

    if seconds < 60:
        return "less than a minute"
    if seconds < 3600:
        return "minutes"
    if seconds < 86400:
        return "hours"
    if seconds <31_536_000:
        return "days to months"
    if seconds <31_536_000 * 100:
        return "years"
    return "centuries+"

def get_recommendations(password: str, entropy_bits: float) -> list[str]:
    recommendations = []
    if len(password) < 8:
        recommendations.append("Use at least 8 characters. NIST requires a minimum of 8.")
    elif len(password) < 15 :
        recommendations.append("Consider using 15+ characters for stronger protection.") 
    else:
        recommendations.append("Good length.")
    
    if entropy_bits < 40:
        recommendations.append("This password has low estimated entropy.")
    elif entropy_bits < 60:
        recommendations.append("This password has moderate estimated entropy.")
    else:
        recommendations.append("This password has a strong estimated entropy.")
    
    recommendations.append("Check the password against known breached password lists.")

    return recommendations

def analyze_password(password:str) ->dict:
    pool_size, sets_used = get_character_pool(password)
    entropy_bits = calculate_entropy(password)
    return {
        "length": len(password),
        "character_pool_size": pool_size, 
        "character_sets": sets_used, 
        "entropy_bits": round(entropy_bits,2),
        "estimated_crack_time": estimate_crack_time(entropy_bits),
        "recommendations": get_recommendations(password, entropy_bits)
    }
