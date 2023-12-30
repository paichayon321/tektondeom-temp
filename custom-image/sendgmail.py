import smtplib
import sys
from email.mime.text import MIMEText
if len(sys.argv) != 6:
    print("Usage: python sendgmail.py sender_mail, sender_password, recipient_email, subject, body ")
    sys.exit(1)

# Get the parameter value from the command line
sender_email = sys.argv[1]
sender_password = sys.argv[2]
recipient_email = sys.argv[3]
subject = sys.argv[4]
body = sys.argv[5]
#body = """
#<html>
#  <body>
#    <p>This is an <b>HTML</b> email sent from Python using the Gmail SMTP server.</p>
#  </body>
#</html>
#"""
html_message = MIMEText(body, 'html')
html_message['Subject'] = subject
html_message['From'] = "PipelineSystem <" + sender_email + ">"
html_message['To'] = recipient_email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
   server.login(sender_email, sender_password)
   server.sendmail(sender_email, recipient_email, html_message.as_string())

print("Email sent to " + recipient_email + " successfully.")

