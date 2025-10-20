import hmac
import base64
import hashlib
import urllib.parse as u
import secrets
import string

def generate_nonce(length: int = 25) -> str:
    """
    Generate a cryptographically secure alphanumeric nonce.
    Default length is 25 (>=16 as required). Uses [A-Za-z0-9].
    """
    alphabet = string.ascii_letters + string.digits  # A-Z a-z 0-9
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def sha256_hex(data: str) -> str:
    # Encode string to bytes, then hash
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def create_signature(method: str, 
                    url: str, 
                    nonce: str, 
                    authDate: str, 
                    access_key: str, 
                    secret_key:str,
                    contentType: str = "") -> str:

    url_path, url_query = u.urlparse(url).path, u.urlparse(url).query

    canonical_string = (
        f"{method}\n"
        f"{nonce}\n"
        f"{authDate}\n"
        f"{contentType}\n"
        f"{url_path}\n"
        f"{url_query}\n"
    ).lower()

    mac_bytes = hmac.new(
        secret_key.encode('utf-8'),
        canonical_string.encode('utf-8'),
        hashlib.sha256
    ).digest()
    hmac_b64 = base64.b64encode(mac_bytes).decode("utf-8")

    signature = f"On {access_key}:HmacSHA256:{hmac_b64}"
    return signature