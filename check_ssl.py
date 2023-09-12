import subprocess
import smtplib
from uuid import uuid4
import inspect
from datetime import datetime, timezone
from unittest.mock import patch

# Send email
def send_email(email_host, email_port, user, password, email_from, email_to, email_body, email_subject):
    
    _user, email_domain = email_from.split('@', 1)
    email_text = inspect.cleandoc(f"""\
    Message-ID: <{uuid4()}@{email_domain}>
    From: Python SMTP Sender <%s>
    To: %s
    Subject: %s

    %s
    """) % (email_from, email_to, email_subject, email_body)
    try:
        smtp = smtplib.SMTP_SSL if email_port == 465 else smtplib.SMTP
        smtp_server = smtp(email_host, email_port)
        smtp_server.ehlo()

        if email_port == 465:
            smtp_server.login(user, password)

        smtp_server.sendmail(email_from, email_to, email_text.encode('UTF-8'))
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)

    return

# E-mail Test Dummy Function
# def send_email(email_from, email_subject, email_body):
#     print("Email sent:")
#     print(f"From: {email_from}")
#     print(f"Subject: {email_subject}")
#     print(f"Body: {email_body}")

def get_open_ssl_output():
    # Construct the command
    command = 'echo|openssl s_client -connect github.com:443 |openssl x509 -noout -dates'
    return subprocess.run(command, shell=True, capture_output=True, text=True, check=True).stdout

def find_ssl(test_result=None):
    
    result = get_open_ssl_output()

    # Extract stdout from CompletedProcess object
    output = test_result or result

    # Split the output into lines
    output_lines = output.strip().split('\n')

    # Find the lines containing certificate dates
    valid_from = None
    valid_until = None
    for line in output_lines:
        if 'notBefore=' in line:
            valid_from = line.split('=')[1].strip()
        elif 'notAfter=' in line:
            valid_until = line.split('=')[1].strip()

    # Update the date format to match the modified format
    date_format = '%b %d %H:%M:%S %Y %Z'
    valid_from_date = datetime.strptime(valid_from, date_format)
    valid_until_date = datetime.strptime(valid_until, date_format)
        
    return valid_from_date, valid_until_date


def main(url, date_threshold=30):
    valid_from_date, valid_until_date = find_ssl()
    
    if valid_from_date and valid_until_date:
        remaining_days = (valid_until_date - datetime.now()).days
        print("{} has {} days remaining on SSL".format(url, remaining_days))
        if remaining_days <= date_threshold:
            # Enter emails details to be sent
            email_from = "your_email@example.com"
            email_subject = "SSL Certificate Expiration Alert"
            email_body = f"The SSL certificate for {url} will expire in {remaining_days} days."
            send_email(email_from, email_subject, email_body)
        else:
            # Reschedule?
            print("OKAY SSL")
            return remaining_days
    else:
        print("Certificate information not found.")


# Test websites
# print(main("ciaobella.obsi.com.au"))
# print(main("unitel.mn"))

