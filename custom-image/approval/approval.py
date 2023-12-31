from flask import Flask, render_template, request
import os
import random
import signal
import sys
import smtplib

from email.mime.text import MIMEText
if len(sys.argv) != 6:
    print("Usage: python sendgmail.py sender_mail sender_password recipient_email approvecode ")
    sys.exit(1)
    
# def generate_random_approval_code():
#     # Generate a random 6-digit approval code (you can adjust the length as needed)
#     return ''.join([str(random.randint(0, 9)) for _ in range(12)])

#Get the parameter value from the command line
sender_email = sys.argv[1]
sender_password = sys.argv[2]
recipient_email = sys.argv[3]
approvecode = sys.argv[4]
tempcode = approvecode
body = "This is approve code: " + tempcode
print("Body: ", body)


html_message = MIMEText(body, 'html')
html_message['Subject'] = "PipelineSystem-ApproveCode"
html_message['From'] = "PipelineSystem <" + sender_email + ">"
html_message['To'] = recipient_email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
   server.login(sender_email, sender_password)
   server.sendmail(sender_email, recipient_email, html_message.as_string())

print("Email sent to " + recipient_email + " successfully.")


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    approval_code = request.form['approval_code']
    action = request.form['action']
    print("TempCode: ", tempcode)    

    # You can add your logic here based on the action (approve or reject)
    if action == 'approve':
        # Perform approval logic
        if approval_code == tempcode:
          result = f'Approval code {approval_code} approved.'
          return render_template('result.html', result=result)
        else:
          result = f'Invalid approve code'
    elif action == 'reject':
        # Perform rejection logic
        if approval_code == tempcode:
          result = f'Approval code {approval_code} rejected.'
          return render_template('result.html', result=result)
    else:
        result = 'Invalid action.'

    return render_template('index.html')

@app.route('/shutdown', methods=['POST'])
def shutdown():
    # This function will be called when the "Done" button is clicked
    print("Shutting down the Flask server...")
    os.kill(os.getpid(), signal.SIGINT)
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
