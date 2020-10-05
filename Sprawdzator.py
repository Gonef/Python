import requests
import gspread
from google.oauth2.service_account import Credentials


scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    scopes=scopes
)


def butcher(temp):
    for counter in range(len(temp)):
        if len(temp[counter]) == 4:
            temp[counter] = int(temp[counter][1:])
    return temp

r = requests.get('https://w43.sfgame.net/req.php?req=0-0tj74j71185Hw1m62ubgJq2WZrleqd11eVcOhgU3DzaEOXqGLGDq63ao04CbIPRzhL1rq99IAO9ineYK2wY_5j6SyW5VrYH-svJQ==&rnd=0.08269227&c=278')
response = str(r.content.decode('utf-8'))
responseSplitted = str(response).split('/')
nicks = response.split('&othergroupmember.s:')[1]
nicks = nicks.split('&othergrouprank')[0]
nicks = nicks.split(',')
# print(nicks)
playersCount = 64 + len(nicks) #64
lvls = responseSplitted[64:playersCount]
lvls = butcher(lvls)
# print(lvls)
temp = zip(nicks,lvls)
guildList = dict(temp)
print(guildList)



gc = gspread.service_account(filename=r'C:\Users\Mateusz\Desktop\Pytong\sf\Sprawdzator-f28421168a94.json')
sh = gc.open_by_key('1sXUYwHXLNuudf_OZsVocAXeQD72ZoBu6uZjZWJfG4Vk')
worksheet = sh.worksheet('2020')


# print(sh.sheet1.get('A1'))
