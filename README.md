
# SSL Certificate Expiry Checker

## How to Use

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/SSL-checker.git
cd SSL-checker
```


### 2. Test the Script (Optional)

Before scheduling periodic checks, you can test the script to ensure it's working as expected:

```bash
python3 check_ssl.py
```

### 3. Schedule Periodic Checks with `cron`

#### On Unix-Like Systems (Linux, macOS)

1. Open the crontab editor:

```bash
crontab -e
```

2. Add the following line to run the script daily at a specific time (e.g., 3:00 PM every Monday):
```
    Schedule a cron job based on the remaining days
    *  *  * * * 
    │  │  │ │ └───── day of the week (0 - 7, both 0 and 7 represent Sunday)
    │  │  │ └─────── month (1 - 12)
    │  │  └───────── day of the month (1 - 31)
    │  └──────────── hour (0 - 23)
    └─────────────── minute (0 - 59)
```
```bash
0 15 * * 1 /usr/bin/python3 /path/to/SSL-checker/check-ssl.py
```


- Replace `/usr/bin/python3` with the path to your Python interpreter.
- Replace `/path/to/SSL-checker/check-ssl.py` with the actual path to your script.

3. Save and exit the crontab editor.

#### On Windows (Task Scheduler)

1. Open the Windows Task Scheduler.

2. Create a new task and configure it to run `python3` with the script's full path as the argument. Set the schedule according to your preferences.

### 4. Monitor SSL Certificates

The script will now run periodically as scheduled, checking the SSL certificates of the specified websites. When a certificate is about to expire within the defined threshold, you can send an email alert.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
