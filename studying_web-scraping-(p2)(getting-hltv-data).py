from bs4 import BeautifulSoup
import requests
import mysql.connector


conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password=''
)
cursor = conn.cursor()
cursor.execute('USE csgo_hltv')

c = 100
date = ''
site = 'https://www.hltv.org/results'

while True:
    c += 100
    try:
        source = requests.get(site).text
    except Exception as error:
        print(error)
    else:
        soup = BeautifulSoup(source, 'lxml')
        for sublist in soup.find_all('div', class_='results-sublist'):
            date = sublist.text[11:40].split('\n')
            date = date[0]
            print(date)
            for match in sublist.find_all('div', class_='result-con'):
                team1 = match.find(
                    'div', class_='line-align team1'
                ).text.replace(
                    '\n', ''
                )
                team2 = match.find(
                    'div', class_='line-align team2'
                ).text.replace(
                    '\n', ''
                )
                result = match.find('td', class_='result-score').text.replace(
                    '\n', ''
                )
                result = result.split(' - ')
                event = match.find('td', class_='event').text.replace('\n', '')
                rec = (
                    'default', team1,
                    team2, result[0],
                    result[1], event,
                    date
                )
                cursor.execute(
                    'INSERT INTO csgo_results_hltv '
                    'VALUES (%s, %s, %s, %s, %s, %s, %s) ',
                    rec
                )
                conn.commit()
            site = 'https://www.hltv.org/results?offset=' + str(c)

conn.commit()
cursor.close()
conn.close()
