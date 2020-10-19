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
        "channelcount" : { "fazerug" : "1683" , "sidemen" : "170" , "sidemenreacts" : "32" , "brawadis" : "1527" , "jj olatunji" : "1030"},
        "playlistcode" : {"fazerug" : "UUilwZiBBfI9X6yiZRzWty8Q" , "sidemen" : "UUDogdKl7t7NHzQ95aEwkdMw" , "sidemenreacts" : "UUjRkTl_HP4zOh3UFaThgRZw" , "brawadis" : "UUvtRTOMP2TqYqu51xNrqAzg" , "jj olatunji" : "UUGmnsW623G1r-Chmo5RB4Yw"}
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
                print(response)  #test run

            elif channelindex[i] in channel["channelID"]:
                requestID = youtube.channels().list(
                    part="statistics",
                    id=channel["channelID"][channelindex[i]],
                    )
                response = requestID.execute()

            else:
                print("NO channel ID found")

            uploadplaylist = channel["playlistcode"][channelindex[i]] # -- get youtube upload playlist code
            print(uploadplaylist)

            for item in response['items']:
                vidcount = item['statistics']['videoCount']

                if vidcount in channel["channelcount"][channelindex[i]] :
                    print("No new upload yet!! --%s" % channelindex[i])
                else:
                    sms = ("New video in *%s* !!!" % channelindex[i])
                    print(sms)
                    print(vidcount)

                    requestcode = youtube.playlistItems().list(
                            part="contentDetails",
                            playlistId=uploadplaylist,
                            maxResults=1,
                            ).execute() # -- get youtube video url code

                    for item in requestcode["items"]:
                        videocode = item["contentDetails"]["videoId"]

                    url = "https://www.youtube.com/watch?v={}".format(videocode)
                    print(url) 
                    message1 = twillio_client.messages.create(body=sms, from_="whatsapp:+14155238886", to="whatsapp:+60176106169") # send alert via whatsapp
                    message2 = twillio_client.messages.create(body=url, from_="whatsapp:+14155238886", to="whatsapp:+60176106169") # send video url via whatsapp

                    print("Alert send!")

                    channel["channelcount"][channelindex[i]] = int(channel["channelcount"][channelindex[i]]) # str to int
                    channel["channelcount"][channelindex[i]] =(channel["channelcount"][channelindex[i]]) + 1
                    channel["channelcount"][channelindex[i]] = str(channel["channelcount"][channelindex[i]]) # int to str

            i = i+1
            time.sleep(10) # wait 10 seconds

        else:
            i=0 # make i = 0 -restart loop


main()
