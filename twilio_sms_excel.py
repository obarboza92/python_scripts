from twilio.rest import Client
import json
import pandas as pd

account_sid = 'ACb8eef81e158531b4d736f37687862342'
auth_token = '142e6b60df4ead9631b5ed426efd4ec3'
client = Client(account_sid, auth_token)
filepath = r"C:\Users\obarb\Downloads\Numbers.xlsx" 

def gather_info_from_excel(filepath):
    """Reads data from Excel and returns names, numbers, and statuses."""
    df = pd.read_excel(filepath)
    names = df['Name'].tolist()
    numbers = df['Number'].tolist()
    status = df['Status'].tolist()
    return names, numbers, status

def filter_pending_recipients(names, numbers, status):
    """Filters recipients with a 'Pending' status."""
    filtered_data = []
    for name, number, st in zip(names, numbers, status):
        if st.lower() == 'pending':
            filtered_data.append((name, number))
    return filtered_data

def send_sms(name, number):
    """Sends an SMS using Twilio."""
    try:
        message = client.messages.create(
            content_sid='HXf357f2d2dcef073d6a3415756876c7be',
            from_='MG8130aba300d8ef903eb567c74fe2c5ea',
            content_variables=json.dumps({'1': name}),
            to=f'+506{number}'
        )
        print(f" Name: {name} | Number: {number} | Message SID: {message.sid} | Status: {message.status}")
    except Exception as e:
        print(f"Error sending message to {name} ({number}): {e}")

# Main program flow
names, numbers, status = gather_info_from_excel(filepath)
pending_recipients = filter_pending_recipients(names, numbers, status)

for name, number in pending_recipients:
    send_sms(name, number)