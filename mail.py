
import smtplib, ssl
import os
from dotenv import load_dotenv  #Used to store credentials
load_dotenv()

def sendEmail(competitions):
    body = ""

    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_PASSWORD")

    receiver_email = "philippquentin6@gmail.com"


    for compet in competitions:
        body+=compet.place+" "+compet.country+"\n"
        for event in compet.events:
            body+="  | "+event.type+" - " + str(event.date)+"\n"
        body+="\n"

    message = 'Subject: {}\n\n{}'.format("FIS Event live", body)

    print(message)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)



if __name__ == "__main__":
    sendEmail([])