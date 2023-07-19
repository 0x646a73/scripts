#!/usr/bin/bash
#
# Outputs status of Mullvad VPN.
#
# If connected, outputs "City, State" of relay node.
# If not connected, outputs status (Off, Connecting, etc.).
#
# Pass a string argument to pad the front and back of output, e.g.
#   $ ./mullvad-status " ~ "
#   > " ~ Prague, Czech Republic ~ "

STATUS=$(mullvad status)
case "$STATUS" in
    Connected*) OUTPUT=$(echo $STATUS | cut -d ' ' -f5-);;
    Disconnected*) OUTPUT="VPN OFF";;
    Connecting*) OUTPUT="Connecting...";;
    Blocked*) OUTPUT="BLOCKED";;
    *) OUTPUT="$STATUS";;
esac

case "$1" in
    *) echo "$1$OUTPUT$1"
esac
