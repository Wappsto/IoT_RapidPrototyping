# Malachite solution

This document provides an example on how to interlink two sensors/actuators. It assumes rapid prototyping has been used to
deploy code to your Porcupine. The code here assmues that a relay and barometer is attached.

## Hint strategy 1: Modify directly on Porcupine

Here we modify the code directly on the Porcupine.

First, use rapid prototyping to generate code and deploy

Next, disable automatic updating of  code  by running `touch ~/wappsto-device.conf`. This ensures that the Porcupine does not lookfor and download deployed code.

Change your workng directory to the dir of the deployed code located in `/opt/wappsto/<uuid>`. E.g. with:

```bash
cd /opt/wappsto/`cat /etc/gatewayid`
```

SSH to the PQPI, and modify code (e.g. using vi) to something like the following. *Note:* the IDs of the generated codes will be different for you.

```python
# Temperature driver mod (add the if-else statement)
def driver_f69d5423_be2c_4b77_af46_20f1ca1717df_callback(name, value, timestamp=None):
    service.get_by_id("f69d5423-be2c-4b77-af46-20f1ca1717df").update(value, timestamp)
    if value > 25:
        relay_driver_bKLJYqwWM2.handle_set("relay", "1")
    else:
        relay_driver_bKLJYqwWM2.handle_set("relay", "0")

# Relay driver mod (comment out the line)
def wappsto_b15bc2f3_f023_4fac_8081_6d5744bc490e_callback(value, action_type):
    if action_type == 'refresh':
        relay_driver_bKLJYqwWM2.handle_refresh("relay")
#    elif action_type == 'set':
#        relay_driver_bKLJYqwWM2.handle_set("relay", value.last_controlled)
```

Reboot the device with the command `reboot`.

## Hint strategy 2: Modify Locally

1. Open the IoT Rapid Prototypig wapp
2. Click on the your assigned prototype
3. Click "..." for the version your are interested (likely the latest)
4. Download and modify code on your laptop as above
5. Copy the modified code to your PQPI
6. Disable the rapid prototype runner with `ssh root@<ip> “touch ~/wappsto-device.conf”`
7. Reboot `reboot` (or restart servies `wappsto-device and rapid-prototype-runer)
