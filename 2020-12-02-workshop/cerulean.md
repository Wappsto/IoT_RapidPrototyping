
# Cerulean solution

## Via Seluxit Device List

1. Download the mobile app
2. In the app, press ⊕
3. Press "Add and configure WiFi".

Notice that your porcupine does not have an WiFi anteanna by default. But it often works OK nevertheless.


## Via `ssh`
You can configure the porcupine WiFi using ssh and configuring the WiFi directly on the porcupine.

First, `ssh` into the porcupine
```
ssh root@<ip> # or
ssh root@PQPI-XXXXXXX
```

Then edit `/etc/wpa_supplicant/wpa_supplicant-wlan0.conf`, e.g. via

```
vi /etc/wpa_supplicant/wpa_supplicant-wlan0.conf
```

to have the content of the network name and password as follows:

```
network={
    ssid="testing"
    psk="testingPassword"
}
```

Verify you have an ip and connection via wlan with `ip a` or `ifconfig`.

Please note: This Is this the "Standard Way" to set up WiFi with the terminal in Linux.
If there is Problem try reset the service:

```
systemctl restart wpa_supplicant@wlan0
```

or reboot the porcupine:

```
reboot
```