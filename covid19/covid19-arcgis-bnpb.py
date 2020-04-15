import json
import requests
from pandas.io.json import json_normalize

import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import datetime

import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def SendEmail(filename, strdate):
    print(filename)
    subject = "Data@Covid19 - " + strdate
    body = "This is an email with attachment sent from Python"
    sender_email = "data@covid19-"+strdate+".com"
    receiver_email = "luckyyuditia.putra@aplcare.com"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        #part.add_header(
        #    "Content-Disposition",
        #    f"attachment; filename= {filename}",
        #)
        
        part.add_header(
            "Content-Disposition"
            ,"attachment; filename={}".format(filename),
        )


        # Add attachment to message and convert message to string
        message.attach(part)
        
        attachment.close()
    
    text = message.as_string()

    # Log in to server using secure context and send email
    with smtplib.SMTP("10.10.12.180") as server:
        server.sendmail(sender_email, receiver_email, text)
        print("OK")


    print("should remove file after send as attachement")
    import os
    os.remove(filename)
    print("File Removed!")
    
    return

urlSource = "https://services5.arcgis.com/VS6HdKS0VfIhv8Ct/arcgis/rest/services/COVID19_Indonesia_per_Provinsi/FeatureServer/0/query?where=1%3D1&outFields=Provinsi,Kasus_Posi,Kasus_Semb,Kasus_Meni&returnGeometry=false&orderByFields=Kasus_Posi%20desc&outSR=&f=json"
response = requests.get(urlSource)
json_data = json.loads(response.text)

df = json_normalize(json_data['features'])

#columns = ['Province', 'Case', 'Health', 'Gone']
df = df.rename(columns={'attributes.Provinsi':'Province', 'attributes.Kasus_Posi':'Positif','attributes.Kasus_Semb':'Health','attributes.Kasus_Meni':'Death'})
#print(df)

strdate = datetime.today().strftime('%Y%m%d')
filename = 'data@covid19-'+ strdate +'.csv'
path = "D:\\" + filename
df.to_csv(path ,index=False)