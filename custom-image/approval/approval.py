from flask import Flask, render_template, request
import os
import random
import signal
import sys

app = Flask(__name__)

def generate_random_approval_code():
    # Generate a random 6-digit approval code (you can adjust the length as needed)
    return ''.join([str(random.randint(0, 9)) for _ in range(12)])

tempcode=generate_random_approval_code()
print("TempCode: ", tempcode)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    approval_code = request.form['approval_code']
    action = request.form['action']


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
