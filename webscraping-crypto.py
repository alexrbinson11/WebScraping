from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

url = 'https://www.cryptoslate.com/coins'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
req = Request(url, headers=headers)

webpage = urlopen(req).read()

soup = BeautifulSoup(webpage, 'html.parser')

print(soup.title.text)

crypto = soup.findAll('tr')

for row in crypto[1:6]:
    td = row.findAll("td")
    name = td[1].find('h3').text.split(" ")[0]
    symbol = td[1].find('span').text
    current = float(td[2].text.replace(',','').split("$")[1])
    change = float(td[3].text.replace('%',''))
    previous = current / (1 + change / 100)

    print(f'\nName: {name}')
    print(f'Symbol: {symbol}')
    print(f'Current Price: ${current:,.2f}')
    print(f'Percent Change in 24 hours: {change}%')
    print(f'Previous Price: {previous:,.2f}')

import keys
from twilio.rest import Client

if name == "Ethereum" and current > 2000:
    client = Client(keys.accountSID, keys.authToken)

    TwilioNumber= "+18446180174"

    mycellphone = "+17144698703"

    textmessage = client.messages.create(to=mycellphone, from_=TwilioNumber, body = "SELL ALERT!: Ethereum is above $2,000 ")  


