# Walkthrough for guardsman red

SSH into your porcupine and do stuff

This walkthrough assumes

* A working porcupine on the same internal network (submask) as you
* Have a linux bash available

You should be able to `ssh` directly to your porcupine  following using

```bash
ssh root@PQPI-XXXXXXXX
```

where `XXXXXXXX` is the first 8 digits of your porcupine UUID.

It that does not work, you need to find the IP of the porcupine. One way is the following:

Find your own IP:

```bash
ip a
# or
ifconfig
# or
ip -o a | awk '/inet / {print $4 "\t: " $2}'
```

And supply the IP to nmap to search for the Porcupine with e.g.

```bash
nmap -sL <ip/mask>
# e.g.
nmap -sL 10.10.70.73/20 | grep "PQPI"
```

## 1. Find OS version details

```bash
uname -a
cat /etc/os-release
cat /etc/build
```

## 2. Find full UUID

To find the full Procupine ID (aka the Procupine Network ID)

```bash
cat /etc/gatewayid
```

## 3. Print out pin header information

Call

```bash
ioinfo
```

For more info, see

```bash
ioinfo --help
```

For example:

```bash
ioinfo -j
```

## 4. Add and remove password

Add password with

```bash
passwd root
```

Enter password, e.g. `guardsmanred`.

Remove password with:

```bash
passwd -d root
```

## 5. Investigate services with systemctl and journalctl ‘wappsto-device’

Get a list the running services:

```bash
systemctl status
```

Of particular interest is 1) `wappsto-device` and 2) `rapid-prototype-uuid`.

```bash
systemctl status rapid-prototype-runner
systemctl status wappsto-device
```

To get the logs from the python program:

```bash
journalctl -u wappsto-device -f
```

Or the logs from the rapid prototype runner:

```bash
journalctl -u rapid-prototype-runner -f
```


## 6. Stop rapid prototype runner

Rapid-prototype-runner is running as a service that *always* downloads the newest deployed code from Wappsto. To disable this, and enable you to change the deployed code, without it getting overwritten.

```bash
touch ~/wappsto-device.conf
```

This simply creates an empty file.



## X. Last factory reset time

Want to know the last time the Porcupine was Factory reset?

```bash
fw_printenv -n factoryreset_confirmation
```
