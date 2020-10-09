import requests
import mysql.connector

#create function for changing 4 digits lvls that don't exist to real ones
def butcher(temp):
    for counter in range(len(temp)):
        if len(temp[counter]) == 4:
            temp[counter] = int(temp[counter][1:])
        else:
            temp[counter] = int(temp[counter])
    return temp

# sending request to get guild list to parse
r = requests.get('https://w43.sfgame.net/req.php?req=0-0tj74j71185Hw1m62ubgJq2WZrleqd11eVcOhgU3DzaEOXqGLGDq63ao04CbIPRzhL1rq99IAO9ineYK2wY_5j6SyW5VrYH-svJQ==&rnd=0.08269227&c=278')
response = str(r.content.decode('utf-8'))
responseSplitted = str(response).split('/')

# getting list of nicks
nicks = response.split('&othergroupmember.s:')[1]
nicks = nicks.split('&othergrouprank')[0]
nicks = nicks.split(',')
playersCount = 64 + len(nicks) #64

# getting list of lvls
lvls = responseSplitted[64:playersCount]
lvls = butcher(lvls)

# creating dictionary with nicks and lvls
temp = zip(nicks,lvls)
guildList = dict(temp)

myDB = mysql.connector.connect(
    user="",
    password="",
    host="",
    database="",
#    auth_plugin='mysql_native_password'
)
cursor = myDB.cursor()

addToTableLvlsUpdate = ("INSERT INTO LvlsUpdate"
                        "(UID, Nick, Lvl) "
                        "VALUES (%s, %s, %s) "
)

addToTablePlayers = ("INSERT INTO Players "
                    "(Nick, Active) "
                    "VALUES (%s, %s)"
)

updateTablePlayers = ("Update Players set Active = %s where Nick = %s "
)

#set active value to 0, so on update it can be changed back to 1
cursor.execute("Update Players set Active = 0")

for player in guildList.keys():
    values = (player, 1)
    print(player) #key
    print(guildList[player]) #value
    try:
        cursor.execute(addToTablePlayers, values)
    except mysql.connector.errors.IntegrityError:
        print("nick " + player + " exist")
        values = (1, player)
        cursor.execute(updateTablePlayers, values)
    myDB.commit()


for player in guildList.keys():
    getUidFromTablePlayers = "select UID from Players where Nick = %s"
    values = (player, )
    cursor.execute(getUidFromTablePlayers, values)
    myresult = cursor.fetchall()
    UID = sum(myresult[0])
    values = (UID, player, guildList[player])
    cursor.execute(addToTableLvlsUpdate, values)
    myDB.commit()

cursor.close()
myDB.close()
