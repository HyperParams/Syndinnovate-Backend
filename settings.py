from dotenv import load_dotenv
import os
from twilio.rest import Client
load_dotenv()
account_sid = 'ACcd8d141a148b8146d9e3d4bcb4ebbee0'
auth_token = '1362785844e526c003c938465a9b7ecf'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+12015089104',
                     to='+919821058706'
                 )

# print(message.sid)
