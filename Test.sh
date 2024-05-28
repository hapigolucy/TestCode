#!/bin/bash

# Function to display usage information
usage() {
    echo "Usage: $0 'account1|platform1|domain1|server1' ['account2|platform2|domain2|server2' ...]"
    echo "   or: $0 -f <file>"
    exit 1
}

# Function to process a single set of arguments
process_args() {
    local arg_set="$1"

    # Split the pipe-separated values into an array
    IFS='|' read -r -a params <<< "$arg_set"

    # Check if we have exactly 4 parameters
    if [ ${#params[@]} -ne 4 ]; then
        echo "Invalid argument set: $arg_set"
        usage
    fi

    account_name="${params[0]}"
    platform="${params[1]}"
    domain="${params[2]}"
    server_name="${params[3]}"

    echo "Running PassMgr with:"
    echo "  Account Name: ${account_name}"
    echo "  Platform: ${platform}"
    echo "  Domain: ${domain}"
    echo "  Server Name: ${server_name}"

    # Call the PassMgr binary with the provided arguments
    ./PassMgr -accountName "${account_name}" -platform "${platform}" -domain "${domain}" -serverName "${server_name}"

    # Check the exit status of the PassMgr call
    if [ $? -eq 0 ]; then
        echo "PassMgr executed successfully for account ${account_name}."
    else
        echo "PassMgr execution failed for account ${account_name}."
    fi
}

# Check if the first argument is '-f' indicating a file input
if [ "$1" == "-f" ]; then
    if [ -z "$2" ]; then
        usage
    fi

    input_file="$2"

    if [ ! -f "$input_file" ]; then
        echo "File not found: $input_file"
        exit 1
    fi

    # Read the file line by line and process each line as arguments
    while IFS= read -r line; do
        process_args "$line"
    done < "$input_file"
else
    # Check if at least one argument is provided
    if [ $# -lt 1 ]; then
        usage
    fi

    # Process each argument set
    for arg_set in "$@"; do
        process_args "$arg_set"
    done
fi

# Call abc.sh after the loop completes
./abc.sh

# Check the exit status of the abc.sh call
if [ $? -eq 0 ]; then
    echo "abc.sh executed successfully."
else
    echo "abc.sh execution failed."
    exit 1
fi

# Call xyz.sh after abc.sh completes
./xyz.sh

# Check the exit status of the xyz.sh call
if [ $? -eq 0 ]; then
    echo "xyz.sh executed successfully."
else
    echo "xyz.sh execution failed."
    exit 1
fi
