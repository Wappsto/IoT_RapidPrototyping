#!/usr/bin/env python3

# This python script demonstrates very basic interactions with Wappsto's RESTful API

# It assumes
# - A Wappsto account
# - A working IoT device with a suitkase relay attached (can be easily modifed with others)
# You need to
# * Correct username and password in the "creds.json" file
# * Correct the following network/porcupine ID to yours
network_uuid = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"

import requests
import json

# Helper functions
def services(endpoint):
    ''' Simply appends the argument to the base url '''
    return(f'https://wappsto.com/services{endpoint}')

def pretty_json_print(x):
    print(json.dumps(x, indent=4, sort_keys=True))

# Setup session
# Start a session
s = requests.Session()

# Get an x-session ID / token
xsession_request = s.post(
    services("/2.0/session"),
    json = json.load(open("2020-12-02-workshop/creds.json", "rb"))
    # json = {'username': "<USERNAME>", 'password': "<PASSWORD>", 'remember_me': True}
)

# Register the x-session ID in the headers
s.headers.update({'x-session': xsession_request.json()["meta"]["id"]})

#
# View all my available networks
#

resp = s.get(services("/network"))
pretty_json_print(resp.json())

#
# Get the specific network of interest
#

r = s.get(services(f'/network/{network_uuid}?expand=3'))
pretty_json_print(r.json())

#
# Turn relay on/off
#

# Automatically find relay control state ID
for device in r.json()['device']:
    if device['product'] == 'SUITKASE_Relay':
        for state in device["value"][0]["state"]:
            if state["type"] == "Control":
                relay_control_state_id = state["meta"]["id"]

print(f'Relay control ID: {relay_control_state_id}')

# # Alternatively, it could have been based on something like:
# r = s.get(services(f'/device?parent_meta.id={network_id}&this_product=SUITKASE_Relay&expand=2')))
# Or simply hard-coding the state id as found in wappsto via the dashboard wapp
# relay_control_state_id = "...."

# Turn relay ON/OFF, "1" for ON, "0" for OFF
data = "0"
r2 = s.patch(services(f'/state/{relay_control_state_id}'),
             json = {"data": data})
