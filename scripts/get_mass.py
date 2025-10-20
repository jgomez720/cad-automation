import requests
import json
import os

env_file = os.getenv('GITHUB_ENV')
print(f"GITHUB_ENV file path: {env_file}")

did = os.environ["ONSHAPE_DID"]
wid = os.environ["ONSHAPE_WID"]
eid = os.environ["ONSHAPE_EID"]

print(f"Document ID: {did}")
print(f"Workspace ID: {wid}")
print(f"Element ID: {eid}")

api_url = f"https://cad.onshape.com/api/partstudios/d/{did}/w/{wid}/e/{eid}/massproperties"

ONSHAPE_SECRET_KEY = os.environ["ONSHAPE_SECRET_KEY"]
ONSHAPE_ACCESS_KEY = os.environ["ONSHAPE_ACCESS_KEY"]

# Define the header for the request 
headers = { 
    'Accept': 'application/json;charset=UTF-8;qs=0.09',
    'Content-Type': 'application/json'
}

params = {}

def get_total_mass() -> float:

    response = requests.get(api_url, 
                    params=params, 
                    auth=(ONSHAPE_ACCESS_KEY, ONSHAPE_SECRET_KEY),
                    headers=headers)
    
    # Check for request errors.
    if response.status_code != 200:
        raise Exception(f"Error fetching mass properties: {response.status_code} - {response.text}")    
    
    # Check to see if the part has a material assigned. 
    if not response.json()["bodies"]["-all-"]["hasMass"]:
        raise Exception("No material assigned to one or more parts in the Part Studio.")
    
    # If no errors, print the response and return the mass value in kg.
    else:
        print(json.dumps(response.json(), indent=4))

        measure_mass_kg = response.json()["bodies"]["-all-"]["mass"][1]

        # Write it so GitHub Actions can use it later
        with open(os.getenv("GITHUB_ENV"), "a") as f:
            f.write(f"MEASURED_MASS_KG=${measure_mass_kg}")
        
        return measure_mass_kg
    
