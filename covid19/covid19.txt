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
    receiver_email = "receipient@email.com"

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
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        
        attachment.close()
    
    text = message.as_string()

    # Log in to server using secure context and send email
    with smtplib.SMTP("filled in with ip hostmail") as server:
        server.sendmail(sender_email, receiver_email, text)
        print("OK")

    print("should remove file after send as attachement")
    import os
    os.remove(filename)
    print("File Removed!")
    
    return

url = "https://www.kompas.com/covid-19"
html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')
#type(soup)

divcovid__row = soup.find_all('div', {"class":"covid__row"})

list = []
for x in divcovid__row:
    prov = x.find("div", {"class":"covid__prov"}).text 
    odp = x.find("span", {"class":"-odp"}).text
    health = x.find("span", {"class":"-health"}).text
    gone = x.find("span", {"class":"-gone"}).text
    list.append([prov, int(re.search(r'\d+', odp).group()), int(re.search(r'\d+', health).group()), int(re.search(r'\d+', gone).group())])
    
columns = ['Province', 'Case', 'Health', 'Gone']
dfcovid = pd.DataFrame(list,columns=columns)

strdate = datetime.today().strftime('%Y%m%d')

filename = 'data@covid19-'+ strdate +'.csv'
dfcovid.to_csv(filename ,index=False)
#dfcovid.to_json(orient='records')

SendEmail(filename, strdate)