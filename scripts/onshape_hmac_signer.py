import hmac
import hashlib
import base64
import uuid
from email.utils import formatdate
from urllib.parse import urlparse


def sign_request(method: str, url: str, access_key: str, secret_key: str, content_type="application/json") -> dict:
    """
    Create the HMAC-signed headers required for authenticating with the Onshape API.

    Args:
        method (str): HTTP method (GET, POST, etc.)
        url (str): Full Onshape API URL
        access_key (str): Onshape API access key
        secret_key (str): Onshape API secret key
        content_type (str): Request Content-Type header (default: application/json)

    Returns:
        dict: Headers including Authorization, Date, Nonce, Content-Type, and Accept.
    """

    # Step 1: Generate Date and Nonce
    date = formatdate(usegmt=True)
    nonce = uuid.uuid4().hex

    # Step 2: Parse the URL
    parsed = urlparse(url)
    path = parsed.path
    query = parsed.query or ""

    # Step 3: Build canonical string
    canonical = "\n".join([
        method.upper(),
        nonce,
        date,
        content_type,
        path,
        query,
        ""
    ]).lower()

    # Step 4: Generate HMAC signature
    signature = base64.b64encode(
        hmac.new(secret_key.encode("utf-8"), canonical.encode("utf-8"), hashlib.sha256).digest()
    ).decode("utf-8")

    # Step 5: Build the headers
    headers = {
        "Date": date,
        "On-Nonce": nonce,
        "Content-Type": content_type,
        "Accept": "application/json",
        "Authorization": f"On {access_key}:HmacSHA256:{signature}",
    }

    return headers
