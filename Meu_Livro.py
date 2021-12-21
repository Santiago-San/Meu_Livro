from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import smtplib
import time
from datetime import datetime


URL = "https://www.amazon.com.br/dp/8575594389/ref=cm_sw_r_wa_apa_glt_i_6PF9BET5C1TFR306GHR1?_encoding=UTF8&psc=1"

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}

site = requests.get(URL, headers=headers)

soup = BeautifulSoup(site.content, 'html.parser')

title =soup.find('span', id = "productTitle", class_ = "a-size-extra-large").get_text()
price = soup.find('span', class_ = 'a-size-base a-color-price a-color-price').get_text()
num_price = price[3:5]
num_price = float(num_price)


def enviar_email():
    message = MIMEMultipart()
    message['From'] = "gabriessga@gmail.com"
    message['To'] = "amanda.arg10@gmail.com"
    message['Subject'] = f"Preço Atual do produto: {title}"

    msg = f"""
O Produto que voce deseja: 
({URL})

                            Esta saindo a um pouco mais de R${num_price}0
"""
    message.attach(MIMEText(msg, 'plain'))
    server = smtplib.SMTP("smtp.gmail.com", port=587)
    server.starttls()
    server.login(message['From'], 'Gabriel@1234567')
    server.sendmail(message['From'], message['To'], message.as_string())
    server.quit()

    print('Sucesso ao enviar o email !!')

def if_price_change():
    atual = 0
    while True:
        if num_price != atual:
            atual = num_price
            enviar_email()
        time.sleep(60)
        print(f'última atualização às {datetime.now().hour}:{datetime.now().minute} de {datetime.now().strftime("%A").lower()}')

if_price_change()