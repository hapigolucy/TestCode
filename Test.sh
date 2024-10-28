#!/bin/bash

# Database connection details
DB_HOST="your_db_host"
DB_PORT="your_db_port"
DB_USER="your_db_user"
DB_PASS="your_db_password"
DB_NAME="your_db_name"

# API details
API_URL="https://your_api_endpoint.com/upload"

# Calculate yesterday's date and adjust for weekends
YESTERDAY=$(date -d "yesterday" +%Y%m%d)
DAY_OF_WEEK=$(date -d "yesterday" +%u)

# If yesterday was Saturday (6), use Friday; if Sunday (7), also use Friday
if [[ "$DAY_OF_WEEK" -eq 6 ]]; then
    YESTERDAY=$(date -d "2 days ago" +%Y%m%d)
elif [[ "$DAY_OF_WEEK" -eq 7 ]]; then
    YESTERDAY=$(date -d "3 days ago" +%Y%m%d)
fi

# Create the rid range
RID_MIN="${YESTERDAY}00"
RID_MAX="${YESTERDAY}99"

# SQL query to fetch the number
SQL_QUERY="SELECT your_number_column FROM your_table WHERE rid > ${RID_MIN} AND rid < ${RID_MAX};"

# Execute the SQL query and fetch the result
# Using 'psql' as an example for PostgreSQL. Modify this part according to your database type.
RESULT=$(PGPASSWORD=$DB_PASS psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "$SQL_QUERY")

# Remove leading/trailing whitespace
RESULT=$(echo "$RESULT" | xargs)

# Check if RESULT is empty
if [[ -z "$RESULT" ]]; then
    echo "No result found for the given query."
    exit 1
fi

# Make the REST API call with curl to upload the result
curl -X POST "$API_URL" -H "Content-Type: application/json" -d "{\"result\": \"$RESULT\"}"

echo "Result uploaded successfully: $RESULT"
