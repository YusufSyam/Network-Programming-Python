import getpass
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64

content = """
отличная игра!
cyka blyat!
"""
# pblptaeeylwszaza
def get_message(sender, receiver):

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = "privet!"
    message.attach(MIMEText(content, "plain"))
    return message

def get_receipt():
    data = []
    with open("email.txt") as file:
        line: str
        for line in file:
            line = line.rstrip('\n').rstrip('\r').strip()
            if line.startswith('#') or len(line) == 0:
                continue
            data.append(line)
    return data

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: %s username" % sys.argv[0])
        sys.exit(1)

    session = smtplib.SMTP("smtp.gmail.com", 587)
    session.starttls()
    session.login(sys.argv[1], getpass.getpass())
    receipt = get_receipt()
    message = get_message(sys.argv[1], ', '.join(receipt)).as_string()
    session.sendmail(sys.argv[1], receipt, message)
    print("Done")
