#!/usr/bin/env python
#
# Outputs status of Mullvad VPN.
#
# If connected, outputs "City, State" of relay node
# If not connected, outputs "OFF"

import subprocess
import sys

state = subprocess.check_output(
                    "mullvad status", shell=True
                    ).decode().strip()
status = "OFF"

if str(state).split()[0] == "Connected":
    status = " ".join(state.split()[-2:])

print(status)
