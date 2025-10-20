import requests
import json
import os
from hmac_signer import create_signature, generate_nonce
from email.utils import formatdate

github_env = os.getenv('GITHUB_ENV')

did = os.environ["ONSHAPE_DID"]
wid = os.environ["ONSHAPE_WID"]
eid = os.environ["ONSHAPE_EID"]

api_url = f"https://cad.onshape.com/api/partstudios/d/{did}/w/{wid}/e/{eid}/massproperties"

ONSHAPE_SECRET_KEY = os.environ["ONSHAPE_SECRET_KEY"]
ONSHAPE_ACCESS_KEY = os.environ["ONSHAPE_ACCESS_KEY"]

nonce = generate_nonce()
current_date = formatdate(usegmt=True)

signature = create_signature(
    method="GET",
    url=api_url,
    nonce=nonce,  
    authDate=current_date,
    # contentType="application/json", not needed for GET
    access_key=ONSHAPE_ACCESS_KEY,
    secret_key=ONSHAPE_SECRET_KEY
)
print(signature)

# Define the header for the request 
headers = {
    "Date": current_date,
    "On-Nonce": nonce,
    "Authorization": signature
}

def get_total_mass() -> float:

    response = requests.get(api_url, headers=headers)
    
    # Check for request errors.
    if response.status_code != 200:
        raise Exception(f"Error fetching mass properties: {response.status_code} - {response.text}")    
    
    else:
        print(json.dumps(response.json(), indent=4))

        measured_mass_kg = response.json()["bodies"]["-all-"]["mass"][1]
        with open(github_env, "a") as f:
            
            f.write(f"MEASURED_MASS_KG={measured_mass_kg}\n")  # no '$', include newline
        
        return measured_mass_kg
    
if __name__ == "__main__":
    total_mass = get_total_mass()
    print(f"Total mass of Part Studio: {total_mass} kg")