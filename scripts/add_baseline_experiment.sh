#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <username> <configuration> <host>"
    exit 1
fi

# Assign arguments to variables
USERNAME=$1
CONFIGURATION=$2
HOST=$3

# Prompt for the password
echo -n "Enter password for $USERNAME: "
read -s PASSWORD
echo

API_URL="https://$HOST/api/login"

# Perform login and save cookies
curl -k -c cookies.txt -X POST $API_URL \
-H "Content-Type: application/json" \
-d "{\"username\":\"$USERNAME\", \"password\":\"$PASSWORD\"}"

# Run the baseline with the provided configuration
curl -k -b cookies.txt -X POST https://$HOST/api/run-baseline \
-F "configuration=@$CONFIGURATION"
