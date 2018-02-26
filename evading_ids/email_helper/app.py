#!flask/bin/python
from flask import Flask, jsonify, request
import smtplib
from email.mime.text import MIMEText
import subprocess

app = Flask(__name__)

me = "friendlyneighbours@sharetravelbucks.com"

def send_mail(share, email):
    print('Sending mail ...')
    msg = MIMEText( "The share for each person is {}.".format(share) )
    msg['Subject'] = "Have no fear! Calculated shares are here!"
    msg['From'] = me
    msg['To'] = email

    s = smtplib.SMTP('localhost', 25)
    s.sendmail(me, [email], msg.as_string())
    s.quit()

    log_cmd = 'touch logs/{}'.format(email)
    print(log_cmd)
    process = subprocess.Popen(log_cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output)
    print('Mail sent!')

@app.route('/api/v1.0/sendmail', methods=['POST'])
def get_bill_total():
    print("REQUEST : {}".format(request))
    share = request.form['share']
    email = request.form['email']
    if share >= 0:
        send_mail(share, email)
    return 'success'  

if __name__ == '__main__':
    app.run(host='192.168.2.14',port=5000)
