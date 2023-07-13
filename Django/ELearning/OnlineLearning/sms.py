import africastalking
import os
import re
from datetime import datetime

# Initialize cache
cache_responses = {}

AfricanTakingUsername = 'justin-nesto10'
AfricanTakingApi = '1084e65964494de4ab714e045fa2757d9c77a214637f674bea0080925c872a24'
# AfricanTakingUsername = 'ArfajaFajanz'
# AfricanTakingApi = '8ac94f43546dfd263d67bed7b87c93d2accfb25e409b6f3cf5de3b523023f9bf'

# Initialize Africa's Talking
username = AfricanTakingUsername
api_key = AfricanTakingApi

africastalking.initialize(username, api_key)


def print_env():
    print(f'username: {username}')
    print(f'api_key: {api_key}')

class SendSMS():
    sms = africastalking.SMS

    def sending(self, phone_number, message):
        # Set the numbers in international format
        recipients = [phone_number,]

        # Set your shortCode or senderId
        # sender = "AFRICASTKNG"

        try:
            response = self.sms.send(message, recipients)
            print(response)
            cache_responses[datetime.now().strftime(
                "%d/%m/%Y")] = sent_number(response["Message"])
            # sample response
            # {
            #     SMSMessageData: {
            #     Message: 'Sent to 1/1 Total Cost: TZS 22.0000',
            #     Recipients: [ [Object] ]
            #     }
            # }
        except Exception as e:
            print(f'Tenemos una problema: {e}')


def sent_number(message: str):
    # input_string = "Sent to 1/1 Total Cost: TZS 22.0000"

    match = re.search(r"Sent to (\d+/\d+)", message)

    if match:
        matched = match.group(1).split("/")
        return {
            "sent": matched[1],
            "received": matched[0]
        }
    else:
        print("None")
