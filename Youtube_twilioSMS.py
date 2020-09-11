from googleapiclient.discovery import build
from twilio.rest import Client
import os
import time

switch = True # Loop NO switch


api_key = os.environ.get("youtubeAPI_key")
twilio_sid = os.environ.get("twilio_SID")
twilio_token = os.environ.get("twilio_TOKEN")

twillio_client = Client(twilio_sid, twilio_token)

youtube = build("youtube", "v3", developerKey=api_key)

request = youtube.channels().list(
    part="statistics",
    forUsername="oRugrat",
    )
response = request.execute()
#print(response)

count = 1665
while switch:
    for item in response['items']:
        vidcount = item['statistics']['videoCount']
        int_video = int(vidcount)

        if (int_video != count):
            print(vidcount)
            message1 = twillio_client.messages.create(body="FaZe Rug new video OUT!!!", from_="whatsapp:+14155238886", to="whatsapp:+60176106169")
            print("New video is OUT!!")
            print("SMS sent!!")
            count=count +1
        else:
            print('No video yet!')

        time.sleep(10) # wait 10 seconds
