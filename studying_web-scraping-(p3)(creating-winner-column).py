import mysql.connector as ms
import pandas as pd


conn = ms.connect(
    host='localhost',
    user='root',
    password=''
)
cursor = conn.cursor()

cursor.execute('USE csgo_hltv')
cursor.execute(
    'SELECT * FROM csgo_results_hltv'
)
rec = cursor.fetchall()

df = pd.DataFrame(
    rec,
    columns=('id', 'team1', 'team2',
             'result team1', 'result team2',
             'event', 'date')
)

cursor.execute(
    'ALTER TABLE csgo_results_hltv '
    'ADD COLUMN winner VARCHAR(25) NOT NULL;'
)

winner = list()
c = 0
for register in rec:
    if int(register[3]) > int(register[4]):
        winner.append(register[1])
    elif int(register[4]) > int(register[3]):
        winner.append(register[2])
    else:
        winner.append(None)
    cursor.execute(
        'UPDATE csgo_results_hltv '
        f'SET `winner` = "{winner[c]}" '
        f'WHERE `id`={c+1}'
    )
    print(c)
    c += 1

df['winner'] = winner

print(df.head())

conn.commit()
cursor.close()
conn.close()
