import subprocess
import smtplib
from uuid import uuid4
import inspect
from datetime import datetime
import os

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
    
    smtp = smtplib.SMTP_SSL if email_port == 465 else smtplib.SMTP
    smtp_server = smtp(email_host, email_port)
    smtp_server.ehlo()

    if email_port == 465:
        smtp_server.login(user, password)

    smtp_server.sendmail(email_from, email_to, email_text.encode('UTF-8'))
    smtp_server.close()
    print ("Email sent successfully!")


    return

def get_open_ssl_output(url):
    # Construct the command
    command = 'echo | openssl s_client -connect {}:443 | openssl x509 -noout -dates'.format(url)
    return subprocess.run(command, shell=True, capture_output=True, text=True, check=True).stdout

def find_ssl(url, test_result=None):

    # Extract stdout from CompletedProcess object
    output = test_result or get_open_ssl_output(url)

    # Find the lines containing certificate dates
    output_dic = dict(line.split('=') for line in output.strip().split('\n'))
    valid_from = output_dic['notBefore']
    valid_until = output_dic['notAfter']

    # Update the date format to match the modified format
    date_format = '%b %d %H:%M:%S %Y %Z'
    valid_from_date = datetime.strptime(valid_from, date_format)
    valid_until_date = datetime.strptime(valid_until, date_format)
        
    return valid_from_date, valid_until_date


def ssl_email_task(url, email_host, email_user, email_password, email_from, email_to, date_threshold=30):

    valid_from_date, valid_until_date = find_ssl(url)
    remaining_days = (valid_until_date - datetime.now()).days
    print("{} has {} days remaining on SSL".format(url, remaining_days))

    if remaining_days <= date_threshold:

        # Enter emails details to be sent
        email_subject = "SSL Certificate Expiration Alert"
        email_body = f"The SSL certificate for {url} will expire in {remaining_days} days."
        email_port = 465
        
        send_email(email_host, email_port, email_user, email_password, email_from, email_to, email_body, email_subject)
    else:
        
        print("SSL Certificate expiration date is acceptable.")
        return remaining_days



# Test websites
# print(main("ciaobella.obsi.com.au"))


if __name__ ==  '__main__':

    email_host = os.environ['EMAIL_HOST']
    email_username = os.environ['EMAIL_USERNAME']
    email_password = os.environ['EMAIL_PASSWORD']
    email_from = os.environ['EMAIL_FROM']
    email_to = os.environ['EMAIL_TO']

    url = 'ciaobella.obsi.com.au'

    ssl_email_task(url, email_host, email_host, email_password, email_from, email_to)
  
