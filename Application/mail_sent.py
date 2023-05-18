from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from jinja2 import Template

SMTP_local_HOST="localhost"
SMTP_local_PORT= 1025
SENDER_ADDRESS = "prasanthisingh2497@gmail.com"
SENDER_PASSWORD = "p1r2a3s4"


def send_email(to_address, subject, message):
    msg=MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(MIMEText(message,"html"))
    
   
    k = smtplib.SMTP(host=SMTP_local_HOST, port=SMTP_local_PORT)

    k.login(SENDER_ADDRESS,"")

    k.send_message(msg)

    k.quit()


    return True 

    
def main():
    send_email("sample@gmail.com", subject="Test mail", message = "hi")


if __name__=="__main__":
    main()