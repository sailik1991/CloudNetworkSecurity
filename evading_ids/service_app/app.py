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
    share = compute_shares(bills, shares)
  
    data = { "email": email, "share": share}
    
    r = requests.post("http://10.218.104.97:5001/api/v1.0/sendmail", data=data)

    print('Requested mail server to send out an email. Return success to user!')  
    return render_template('success.html')

if __name__ == '__main__':
    app.run(host='192.168.1.12',port=5002)
