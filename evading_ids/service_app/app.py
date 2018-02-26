#!flask/bin/python
from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)

def compute_shares(bills, shares):
    total = sum([float(x.strip()) for x in bills.split(',')])
    shares = int(shares)
    print(total, shares)
    return (total/shares)    

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/getShares', methods=['GET'])
def getShares():
    bills = request.args.get('bills')
    shares = request.args.get('shares')
    email = request.args.get('email')
    try:
        share = compute_shares(bills, shares)
    except:
        fail_str = 'Unfortunately, there was an error processing the request! Please try again and make sure that the inputs are in the correct format.'
        print(fail_str)
        return render_template('index.html', message_f=fail_str)
    data = { "email": email, "share": share}
    
    r = requests.post("http://192.168.2.14:5000/api/v1.0/sendmail", data=data)

    sucs_str = 'We are processing your request... You will get a mail from us shortly!'
    print(sucs_str)
    return render_template('index.html', message_s=sucs_str)

if __name__ == '__main__':
    app.run(host='192.168.1.12',port=5000)
