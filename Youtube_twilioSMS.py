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

channelindex = ("fazerug", "sidemen", "sidemenreacts", "brawadis", "jj olatunji" )
channel = {"channelID" : { "sidemen" : "UCDogdKl7t7NHzQ95aEwkdMw" , "sidemenreacts" : "UCjRkTl_HP4zOh3UFaThgRZw" , "brawadis" : "UCvtRTOMP2TqYqu51xNrqAzg" },
        "channelUsername" : { "fazerug" : "oRugrat" , "jj olatunji" : "KSIOlajidebtHD"},
        "channelcount" : { "fazerug" : "1667" , "sidemen" : "165" , "sidemenreacts" : "16" , "brawadis" : "1509" , "jj olatunji" : "1017"}
        }

def stat_request():

    #youtube channel ID request
    requestID = youtube.channels().list(
        part="statistics",
        id="UCjRkTl_HP4zOh3UFaThgRZw",
        )
    #youtube channel Username request
    request_username = youtube.channels().list(
        part="statistics",
        forUsername="oRugrat, KSIOlajidebtHD",
        )
    response = request_username.execute()
    print(response)



def main():
    i = 0
    while switch:
        if (i <= 4): # complete one cycle
            if channelindex[i] in channel["channelUsername"]:
                request_username = youtube.channels().list(
                    part="statistics",
                    forUsername=channel["channelUsername"][channelindex[i]],
                    )
                response = request_username.execute()

            elif channelindex[i] in channel["channelID"]:
                requestID = youtube.channels().list(
                    part="statistics",
                    id=channel["channelID"][channelindex[i]],
                    )
                response = requestID.execute()

            else:
                print("NO channel ID found")

            for item in response['items']:
                vidcount = item['statistics']['videoCount']

                if vidcount in channel["channelcount"][channelindex[i]] :
                    print("No new upload yet!! --%s" % channelindex[i])
                else:
                    sms = ("New video in *%s* !!!" % channelindex[i])
                    print(sms)
                    print(vidcount)
                    message1 = twillio_client.messages.create(body=sms, from_="whatsapp:+14155238886", to="whatsapp:+60176106169") # send alert via whatsapp
                    print("Alert send!")
                    channel["channelcount"][channelindex[i]] = int(channel["channelcount"][channelindex[i]]) # str to int
                    channel["channelcount"][channelindex[i]] =(channel["channelcount"][channelindex[i]]) + 1
                    channel["channelcount"][channelindex[i]] = str(channel["channelcount"][channelindex[i]]) # int to str

            i = i+1
            time.sleep(2) # wait 10 seconds

        else:
            i=0 # make i = 0 -restart loop


main()
