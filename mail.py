
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import date
import json

from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv  #Used to store credentials
load_dotenv()


def getLiveCompetition(dateEvent):

    print(f"Check live event for {dateEvent}")
    competitionList = []

    with open("results.json",'r') as results:
        data = json.load(results)

    for competition in data:
        # If the provided date is in between the start and the end of the event
        if competition["startDate"]["year"] <= dateEvent.year and \
        competition["startDate"]["month"] <= dateEvent.month and \
        competition["startDate"]["day"] <= dateEvent.day and \
        competition["endDate"]["year"] >= dateEvent.year and \
        competition["endDate"]["month"] >= dateEvent.month and \
        competition["endDate"]["day"] >= dateEvent.day:


            # If there is a competition with the date provided. Sometime an event can be 4 days long with only 2 races
            for event in competition["events"]:
                if event["date"]["day"] == dateEvent.day:
                    competitionList.append(competition)
                    break

    return competitionList


def sendHTMLEmail(dateEvent=None):

    if dateEvent==None:
        dateEvent = date.today()



    # Get all competitions on live at this date
    competitions = getLiveCompetition(dateEvent)


    if competitions :
        # Load email struct
        with open("emailBase.html","r") as html:
            htmlContent = html.read()

        htmlToAdd=""
        for compet in competitions:
            with open("event.html","r") as eventHtml:
                eventHtmlStr = eventHtml.read()

                #fill HTML template
                eventHtmlStr = eventHtmlStr.replace('{{title}}',compet['place']+" "+compet["country"])
                eventsStr=""
                for event in compet['events']:
                    if event["date"]["day"]==dateEvent.day:
                        eventsStr += "<p style='font-size: 25px'>"+event["type"]+" - " + str(event["date"]["year"])+"/"+ str(event["date"]["month"])+"/"+ str(event["date"]["day"])+" "+ str(event["date"]["hour"])+":"+ str(event["date"]["min"])+"</p>"
                    else:
                        eventsStr += "<p style='font-size: 18px'>"+event["type"]+" - " + str(event["date"]["year"])+"/"+ str(event["date"]["month"])+"/"+ str(event["date"]["day"])+" "+ str(event["date"]["hour"])+":"+ str(event["date"]["min"])+"</p>"



                eventHtmlStr = eventHtmlStr.replace('{{race}}',eventsStr)

                htmlToAdd += eventHtmlStr

        htmlContent = htmlContent.replace('{{event}}',htmlToAdd)



        smtp_server = "smtp.gmail.com"
        sender_email = os.getenv("GMAIL_USER")
        password = os.getenv("GMAIL_PASSWORD")

        receiver_email = "philippquentin6@gmail.com"

        message = MIMEMultipart("alternative")
        message["Subject"] = "FIS Live today"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Attach FIS logo
        fp = open('fis.png', 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<image>')
        message.attach(msgImage)

        # Turn these into html MIMEText objects
        part1 = MIMEText(htmlContent, "html")

        message.attach(part1)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
    else:
        print("No competition today")
if __name__ == "__main__":
    # sendEmail([])
    dateEvent = date.fromisoformat('2020-12-29')
    sendHTMLEmail(dateEvent)
    # sendHTMLEmail()