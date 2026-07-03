import ipaddress

def validate_ip(ip_str: str) -> bool:
    """Validates if a given string is a syntactically correct IPv4 or IPv6 address."""
    try:
        ipaddress.ip_address(ip_str.strip())
        return True
    except ValueError:
        return False

def get_flag_emoji(country_code: str) -> str:
    """Converts a standard two-letter ISO country code into its corresponding flag emoji."""
    if not country_code or len(country_code) != 2:
        return "🏳️"
    return "".join(chr(ord(char.upper()) + 127397) for char in country_code)
