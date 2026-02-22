#!/bin/bash
#
# Connect to random vpn endpoint
#
# Required environment variables:
#  - purevpn_username
#  - purevpn_password

set -e

# verify PureVPN installed
if ! which purevpn > /dev/null; then
    echo "ERROR: purevpn package is missing"
    exit 2
fi

ORIG_IP=$(curl -s 'icanhazip.com')
echo "Current IP: ${ORIG_IP}"

# start purevpn service
service purevpn start

# login to purevpn
expect <<EOD
spawn purevpn --login
expect "Username:"
send "${purevpn_username}\r"
expect "Password:"
send "${purevpn_password}\r"
expect #
EOD

# get all location codes
LOCATIONS=$(purevpn --location | grep -o -E '[A-Z]{2}')
ARRAY=(${LOCATIONS//:/ })
LEN=${#ARRAY[@]}

# select random one
RANDOM_LOCATION=${ARRAY[$((RANDOM % $LEN))]}

# connect
echo "Connecting to ${RANDOM_LOCATION}..."
purevpn --connect "${RANDOM_LOCATION}"

# fix resolve
echo "nameserver 8.8.8.8" > /etc/resolv.conf

service purevpn restart

NEW_IP=$(curl -s 'icanhazip.com')
echo "Original IP: ${ORIG_IP}"
echo "New IP (${RANDOM_LOCATION}): ${NEW_IP}"

exec "$@"
