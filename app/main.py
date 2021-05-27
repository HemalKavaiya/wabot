from flask import Flask, request
import requests
import datetime 
from datetime import datetime
from twilio.twiml.messaging_response import MessagingResponse
from flask import session

app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'vaccine' in incoming_msg:
        pin = 380008
        today = datetime.today().strftime('%d-%m-%Y')
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pin,today)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(URL,headers=headers)
        if r.status_code == 200:
            data = r.json()
            centers = data['centers']
            for center in centers:
                for session in center["sessions"]:
                    if session["min_age_limit"] <= 21:
                        if session["available_capacity"] > 0:
                            subject = 'Covid-Vaccine availability'
                            message = "\t {}\n\t {}\n\t Time: {} To {}\n\t Price: {}\n\t Available Capacity: {}\n\t Vaccine: {}".format(center["name"],center['address'],center["from"],center["to"],center["fee_type"],session["available_capacity"],session["vaccine"])
                            print("\t", center["name"])
                            print("\t", center["address"])
                            print("\t Time: ", center["from"]+" TO "+center["to"])
                            print("\t Price: ", center["fee_type"])
                            print("\t Available Capacity: ", session["available_capacity"])
                            if(session["vaccine"] != ''):
                                print("\t Vaccine: ", session["vaccine"])
                            print("\n\n")
                        else:
                            message = "No session available right now"
        msg.body(message)
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    if not responded:
        msg.body('I only know about famous quotes and cats, sorry!')
    return str(resp)


if __name__ == '__main__':
    app.run()