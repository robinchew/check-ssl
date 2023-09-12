import subprocess
from datetime import datetime
from check_ssl import main  

# Replace with your URL and desired email recipient
url = "ciaobella.obsi.com.au"
recipient_email = "example@example.com"

# Call the main function to get the remaining days until expiration
remaining_days = main(url, date_threshold=30)

if remaining_days is not None:
    # Schedule a cron job based on the remaining days
    # *  *  * * * 
    # │  │  │ │ └───── day of the week (0 - 7, both 0 and 7 represent Sunday)
    # │  │  │ └─────── month (1 - 12)
    # │  │  └───────── day of the month (1 - 31)
    # │  └──────────── hour (0 - 23)
    # └─────────────── minute (0 - 59)
    if remaining_days <= 7:
        # If expiration is within 7 days, schedule daily
        cron_schedule = "0 9 * * *"
    else:
        # If expiration is more than 7 days away, schedule weekly
        cron_schedule = "0 9 * * 1"

    cron_command = f"python check_ssl.py"
    print(subprocess.run(f'(crontab -l ; echo "{cron_schedule} {cron_command}") | crontab -', shell=True))

