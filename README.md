# kali-ip-changer
kali-ip-changer/ 
# Install prereqs once:

sudo apt update

sudo apt install python3-pip tor

pip3 install requests[socks] stem


**Usage Examples**
1) Infinite rotation every 60 seconds (default)
   
sudo tor &             # ensure Tor is running

python3 fast_tor_ip.py

2)- Rotate 10 times at 30 s interval:

python3 fast_tor_ip.py -n 10 -i 30

3)- If you’ve set a ControlPort password in /etc/tor/torrc:

python3 fast_tor_ip.py -p your_tor_password

Next Steps

- Hook this into a systemd service or cron job for unattended rotation
- 
- Add logging to a file for audit or debugging
- 
- Combine with your existing tooling (scans, scrapers, API calls) in one script
- 
- Wrap it in a simple CLI menu or web UI for point-and-click control



for more information follow on insta : https://www.instagram.com/__golu__maurya__
