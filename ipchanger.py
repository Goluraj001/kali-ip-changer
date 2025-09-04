#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fast Tor-based IP Changer for Kali/Debian
Uses the Tor ControlPort to SIGNAL NEWNYM (new circuit)
instead of reloading the whole service.
"""

import time
import sys
import argparse

import requests
from stem import Signal
from stem.control import Controller

# default ports
TOR_SOCKS_PORT   = 9050
TOR_CONTROL_PORT = 9051

def get_current_ip():
    """
    Fetch your current public IP via checkip.amazonaws.com
    over Tor SOCKS5 proxy.
    """
    session = requests.Session()
    session.proxies = {
        'http':  f'socks5h://127.0.0.1:{TOR_SOCKS_PORT}',
        'https': f'socks5h://127.0.0.1:{TOR_SOCKS_PORT}',
    }
    try:
        resp = session.get('http://checkip.amazonaws.com', timeout=10)
        return resp.text.strip()
    except Exception as e:
        return f"Error fetching IP: {e}"

def renew_tor_identity(control_pass=None):
    """
    Connect to Tor ControlPort and send NEWNYM signal
    """
    with Controller.from_port(port=TOR_CONTROL_PORT) as ctl:
        if control_pass:
            ctl.authenticate(password=control_pass)
        else:
            ctl.authenticate()  # assumes cookie-auth or no auth
        ctl.signal(Signal.NEWNYM)

def main():
    parser = argparse.ArgumentParser(description="Fast Tor IP Changer")
    parser.add_argument(
        '-n', '--count', type=int, default=0,
        help='Number of times to rotate (0 = infinite)'
    )
    parser.add_argument(
        '-i', '--interval', type=int, default=60,
        help='Seconds between each IP change'
    )
    parser.add_argument(
        '-p', '--password', default=None,
        help='Tor ControlPort password (if set in torrc)'
    )
    args = parser.parse_args()

    print(f"[+] Starting Fast Tor IP Changer: interval={args.interval}s, "
          f"{'infinite' if args.count==0 else args.count} rotations\n")

    iteration = 0
    try:
        while True:
            iteration += 1
            print(f"--- Iteration #{iteration} ---")

            print("[*] Requesting new Tor circuit…", end=' ')
            renew_tor_identity(control_pass=args.password)
            print("done.")

            # give Tor a moment to build that new circuit
            time.sleep(3)

            ip = get_current_ip()
            print(f"[+] New exit IP: {ip}\n")

            if args.count and iteration >= args.count:
                print("[*] Reached requested rotation count. Exiting.")
                break

            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\n[*] Interrupted by user. Exiting.")
        sys.exit(0)


if __name__ == "__main__":
    main()
