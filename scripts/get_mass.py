import requests
import json
import os

did = os.environ["ONSHAPE_DID"]
wid = os.environ["ONSHAPE_WID"]
eid = os.environ["ONSHAPE_EID"]

api_url = f"https://cad.onshape.com/api/partstudios/d/{did}/w/{wid}/e/{eid}/massproperties"

SECRET_KEY = os.environ["SECRET_KEY"]
ACCESS_KEY = os.environ["ACCESS_KEY"]

# Define the header for the request 
headers = { 
    'Accept': 'application/json;charset=UTF-8;qs=0.09',
    'Content-Type': 'application/json'
}

params = {}

def get_total_mass() -> float:

    response = requests.get(api_url, 
                    params=params, 
                    auth=(ACCESS_KEY, SECRET_KEY),
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

        return response.json()["bodies"]["-all-"]["mass"][1]
    
get_total_mass()