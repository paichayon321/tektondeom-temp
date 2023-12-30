from flask import Flask, render_template, request

app = Flask(__name__)

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
        result = f'Approval code {approval_code} approved.'
    elif action == 'reject':
        # Perform rejection logic
        result = f'Approval code {approval_code} rejected.'
    else:
        result = 'Invalid action.'

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
