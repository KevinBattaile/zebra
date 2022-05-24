#!/bin/bash
HERE="$(dirname "$0")"
# Take the PV prefix from the first argument from the script if supplied
# This must be specified if there are more than one instances of the IOC on
# the network
# Default gives PVs that look like TESTZEBRA:AND1_INV
PREFIX="${1:-TESTZEBRA}"
# By default /dev/ttyUSB0 is not readable or writeable, make it so
[ -e /dev/ttyUSB0 ] || {
    echo /dev/ttyUSB0 does not exist, please plug in Zebra via a USB-RS232 converter;
    exit 1
}
[ -w /dev/ttyUSB0 ] || sudo chmod a+rw /dev/ttyUSB0
# Max sure we have enough space to store 100000 doubles
export EPICS_CA_MAX_ARRAY_BYTES=801000
# Start the IOC
gnome-terminal -e "${HERE}/iocs/test/bin/linux-x86_64/sttest.sh ${PREFIX}" &
# Start the Gui
"${HERE}/zebraGui/zebraGui" "${PREFIX}" &
