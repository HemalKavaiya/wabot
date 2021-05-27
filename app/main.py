from flask import Flask, request
import requests
import datetime 
from datetime import datetime
from twilio.twiml.messaging_response import MessagingResponse
from flask import session

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False

    print(incoming_msg)
    if 'Hi' in incoming_msg or 'Hey' in incoming_msg or 'Heya' in incoming_msg or 'Menu' in incoming_msg:
        text = f'Hello 🙋🏽‍♂, \nThis is a Cowin-Bot developed by https://github.com/HemalKavaiya to provide latest information about vaccination.\n\n Please enter one of the following option 👇 \n *slots*. It will check for available slots*.'
        msg.body(text)
        responded = True

    if not responded:
        msg.body("Can't understand your request, try again")
    return str(resp)

if __name__ == '__main__':
    app.run()