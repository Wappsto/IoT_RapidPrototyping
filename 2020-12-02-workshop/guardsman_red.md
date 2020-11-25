# Walkthrough for guardsman red

It assumes
 - A working porcupine on the same internal network (submask) as you
 - Have a linux bash

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

## Find full UUID

```
cat /etc/gatewayid
```


## Find OS version details

```
uname -a
cat /etc/os-release
cat /etc/build
```

## Set password

```
passwd root
```

Enter password, e.g. `guardsmanred`

## Remove password again

```
passwd -d root
```
