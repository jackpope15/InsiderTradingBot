import requests
from bs4 import BeautifulSoup
from csv import writer


cookies = {
    'PHPSESSID': 'dv492sdpcsatdksi6m4i0kau80',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://www.secform4.com/account/WatchAlerts.php',
    'Accept-Language': 'en-US,en;q=0.9',
}

response = requests.get('https://www.secform4.com/buying.htm', headers=headers, cookies=cookies)

soup = BeautifulSoup(response.text, 'html.parser')

stocks = soup.find(class_='sort-table')

with open('InsiderStocks.csv', 'w') as csv_file:
    csv_writer = writer(csv_file)
    headers = ['Date', 'ID', 'Amount']
    csv_writer.writerow(headers)

    for tr in stocks.findAll('tr'):
        text = [x.text for x in tr.findAll('td')]
        dollarAmount = text[7]
        dollarAmount = dollarAmount[1:].replace(',', '')
        try:
            amount = float(dollarAmount)
            if(amount >= 5000000):
                stock_id = text[3]
                if(len(stock_id) == 0):
                    stock_id = text[2]
                
                date = text[0][:-8]
                csv_writer.writerow([date, stock_id, amount])
        except:
            print('Unable to parse dollarAmount into a viable float')