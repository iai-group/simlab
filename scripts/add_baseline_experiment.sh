#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <username> <configuration>"
    exit 1
fi

# Assign arguments to variables
USERNAME=$1
CONFIGURATION=$2

# Prompt for the password
echo -n "Enter password for $USERNAME: "
read -s PASSWORD
echo

API_URL="https://localhost/api/login"

# Perform login and save cookies
curl -k -c cookies.txt -X POST $API_URL \
-H "Content-Type: application/json" \
-d "{\"username\":\"$USERNAME\", \"password\":\"$PASSWORD\"}"

# Run the baseline with the provided configuration
curl -k -b cookies.txt -X POST https://localhost/api/run-baseline \
-F "configuration=@$CONFIGURATION"
