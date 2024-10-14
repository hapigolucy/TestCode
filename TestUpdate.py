DAYS_SINCE_ROTATION=$(( ( $(date +%s) - $(date -d "$LAST_ROTATION_DATE" +%s) ) / 86400 ))

import os
from datetime import datetime, timedelta
import subprocess

# File where last updation date is stored
LAST_updation_FILE = "/path/to/last_updation_date.txt"
# Path to the cwd updation script
cwd_updation_SCRIPT = "/path/to/cwd_updation_script.sh"

def get_last_updation_date():
    """Reads the last updation date from the file."""
    if not os.path.exists(LAST_updation_FILE):
        # If the file doesn't exist, set today's date as the first updation date
        with open(LAST_updation_FILE, 'w') as file:
            today = datetime.today().strftime('%Y-%m-%d')
            file.write(today)
        return datetime.today()
    
    with open(LAST_updation_FILE, 'r') as file:
        last_updation_date_str = file.read().strip()
    
    # Convert the string into a datetime object
    return datetime.strptime(last_updation_date_str, '%Y-%m-%d')

def update_last_updation_date():
    """Updates the last updation date in the file to today."""
    today = datetime.today().strftime('%Y-%m-%d')
    with open(LAST_updation_FILE, 'w') as file:
        file.write(today)

def update_cwds():
    """Function to update cwds by calling the cwd updation script."""
    print("Rotating cwds...")
    # Run the cwd updation shell script using subprocess
    subprocess.run([cwd_updation_SCRIPT], check=True)
    
    # Update the last updation date
    update_last_updation_date()

def main():
    # Get the last updation date
    last_updation_date = get_last_updation_date()
    
    # Calculate the number of days since the last updation
    days_since_updation = (datetime.today() - last_updation_date).days
    
    # Check if today is Saturday (5 = Saturday, because Python's weekday starts at 0 = Monday)
    is_saturday = datetime.today().weekday() == 5
    
    # update cwds if 300+ days have passed and today is Saturday
    if days_since_updation >= 300 and is_saturday:
        update_cwds()
    else:
        print("cwd updation is not required today.")

if __name__ == "__main__":
    main()
