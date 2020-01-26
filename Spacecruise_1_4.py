import mysql.connector
import os
import random

#Connect to database
db = mysql.connector.connect(host="localhost",
                      user="dbuser",
                      passwd="dbpass",
                      db="spacecruise",
                      buffered=True)
def enemycheck():
    cur = db.cursor()
    enemyalivesql = """select enemy.health_points from enemy where enemy.roomid = %s""" % (location)
    cur.execute(enemyalivesql)
    for row in cur.fetchall():
        return row[0]

def playercheck():
    cur = db.cursor()
    playeralivesql = """select playable_character.health_points from playable_character"""
    cur.execute(playeralivesql)
    for row in cur.fetchall():
        alive = int(row[0])
    if alive >=0:
        status = 0
    else:
        status = 1
    return status
        
    

def combat():
    alive = 1
    enemyalive = 1
    print (" ")
    print (" ")
    print ("While in a gunfight you can either 'shoot' or attempt to 'run")
    print (" ")
    print (" ")
    print (" ")
    while alive >= 1 and enemyalive >= 1:
        combatcmd = input("What do you want to do?: ")
        if combatcmd == "shoot":
            cur = db.cursor()
            playeralivesql = """select playable_character.health_points from playable_character"""
            cur.execute(playeralivesql)
            for row in cur.fetchall():
                alive = int(row[0])
            if alive >0:
                shoot()
                print (" ")
            else:
               print ("Your enemy was a better shooter")
            enemyalivesql = """select enemy.health_points from enemy where enemy.roomid = %s""" % (location)
            cur.execute(enemyalivesql)
            for row in cur.fetchall():
                enemyalive = int(row[0])
            if enemyalive >0:
                getshot()
                playeralivesql = """select playable_character.health_points from playable_character"""
                cur.execute(playeralivesql)
                for row in cur.fetchall():
                    alive = int(row[0])
                    print (" ")
            else:
                print ("You killed your enemy!")
                
        elif combatcmd == "run":
            escape = random.randint(1,10)
            if escape <= 4:
                print ("You run back to the hallway")
                curhealth()
                fallback = 7
                return fallback
            else:
                print ("Your enemy blocks your path and takes a shot")
                getshot()
                cur = db.cursor()
                cur.execute("""select playable_character.health_points from playable_character""")
                for row in cur.fetchall():
                    alive = int(row[0])
        else:
            print ("Invalid input")
        
    return location

def shoot():
    cur = db.cursor()
    sql = """select item.id from item join playable_character on item.playerid =playable_character.id join item_type on item_type.id = item.itemtypeid where item.itemtypeid=1 or item.itemtypeid=2 or item.itemtypeid=3 and item.playerid=1"""
    cur.execute(sql)
    if cur.rowcount >=1:
        #tähän combat juttu
        combatsql = """select max(item.itemtypeid) from item join item_type on item_type.id = item.ItemTypeID where item.playerid is not null and item_type.ID <4"""
        cur.execute(combatsql)
        for row in cur.fetchall():
            gunid = row[0]
            combatsql2 = """select attack_accuracy from item_type where item_type.id = %s""" % (gunid)
            cur.execute(combatsql2)
            for row in cur.fetchall():
                acc = row[0]
    else:
        print ("You entered a gunfight without a gun!")
        cur.execute('UPDATE playable_character SET health_points = 0')
          
    combatsql3 = """select enemy.combat_difficulty from enemy where enemy.roomid = %s""" % (location)
    cur.execute(combatsql3)
    for row in cur.fetchall():
        difficulty = row[0]
        shot = random.randint(1,difficulty)
        if acc >= shot:
            damagesql = """select hp_effect from item_type where item_type.id = %s""" % (gunid)
            cur.execute(damagesql)
            for row in cur.fetchall():
                damage = row[0]
                print ("You hit your target for",damage)
            enemyhpsql = """select enemy.health_points from enemy where enemy.roomid = %s""" % (location)
            cur.execute(enemyhpsql)
            for row in cur.fetchall():
                enemyhp = row[0]
                newenemyhp = (int(enemyhp+(int(damage))))
                newenemyhpsql = """update enemy set enemy.health_points = %s where enemy.roomid= %s""" % (newenemyhp,location)
                cur.execute(newenemyhpsql)
                print("Your enemy has",newenemyhp,"hp remaining")
            
        else:
            print ("You missed!")

def getshot():
    cur = db.cursor()
    sql = """select item.id from item join enemy on item.id =enemy.id join item_type on item_type.id = item.itemtypeid where item.itemtypeid=1 or item.itemtypeid=2 or item.itemtypeid=3 and enemy.roomid= %s""" % (location)
    cur.execute(sql)
    if cur.rowcount >=1:
        #tähän combat juttu
        combatsql = """select max(item.itemtypeid) from item join item_type on item_type.id = item.ItemTypeID join enemy on enemy.id = item.enemyid where enemy.roomid = %s and item_type.ID <4""" % (location)
        cur.execute(combatsql)
        for row in cur.fetchall():
            gunid = row[0]
            combatsql2 = """select attack_accuracy from item_type where item_type.id = %s""" % (gunid)
            cur.execute(combatsql2)
            for row in cur.fetchall():
                acc = row[0]
    else:
      print ("Error 1")
      #tähän asti toimii
    combatsql3 = """select playable_character.combat_difficulty from playable_character where playable_character.id = 1"""
    cur.execute(combatsql3)
    for row in cur.fetchall():  
        difficulty = row[0]
        shot = random.randint(1,difficulty)
    if acc >= shot:
        damagesql = """select hp_effect from item_type where item_type.id = %s""" % (gunid)
        cur.execute(damagesql)
        for row in cur.fetchall():
            damage = row[0]
            print ("You were hit for",damage)
        playerhpsql = """select playable_character.health_points from playable_character where playable_character.id = 1"""
        cur.execute(playerhpsql)
        for row in cur.fetchall():
            playerhp = row[0]
            newplayerhp = (int(playerhp+(int(damage))))
            newplayerhpsql = """update playable_character set playable_character.health_points = %s""" % (newplayerhp)
            cur.execute(newplayerhpsql)
            print("You have",newplayerhp,"hp remaning.")
    else:
        print ("Your enemy missed!")
            

def checkammo(): #Print total ammo count
    cur = db.cursor()
    sql = """select sum(item_type.ammo) from item_type join item on item_type.id = item.ItemTypeID where item_type.name ="ammo" and item.playerid=1"""
    cur.execute(sql)
    if cur.rowcount >=1:
        for row in cur.fetchall():
            if row[0] == None:
                total = 0
            else:
                total = row[0]
    return total
        
def checkhelmet(): # Check if the player has a helmet when entering control room
    cur = db.cursor()
    sql = """SELECT * FROM item
WHERE item.id = 6 AND item.playerid = 1"""
    cur.execute(sql)
    if cur.rowcount==1:
        print ("One of the pirates shoots you in the head. Your helmet ricochets the bullet and you imemdiately shoot back, killing the pirate. Now you are facing just one more enemy")
        leave = 0
        return leave
    else:
        leave = 1
        print ("One of the pirates shoots you in the head. If you only had a helmet to protect yourself!")
        print ("You died!")
        return leave
    
def description(location, target): #Target details
    cur = db.cursor()
    sql = """SELECT description.Details FROM description
JOIN room ON description.roomid = room.roomid
WHERE (description.roomid = (%s)) AND (description.name = '%s')""" % (location, target)
    cur.execute(sql)
    if cur.rowcount==0:
        cur = db.cursor()
        sql2 = """SELECT item_type.details FROM item_type
JOIN item on item.itemtypeid = item_type.id join room ON item.roomid = room.roomid
WHERE (item.roomid = (%s)) AND (item_type.name = '%s')""" % (location, target)
        cur.execute(sql2)
        if cur.rowcount>=1:
            for row in cur.fetchall():
               print (row[0])
        else:
            print ("There is nothing.")
        return
    if cur.rowcount>=1:
        for row in cur.fetchall():
           print (row[0])
           return

def movement(location,direction): #Check if input is valid
    cur = db.cursor()
    sql = """SELECT ToID FROM Moving WHERE Direction = (%s) AND FromID = (%s) AND LOCKED = 0""" % (direction, location)
    cur.execute(sql)
    if cur.rowcount>=1:
        for row in cur.fetchall():
            destination = row[0] #Set new location
            return destination
    else: #Check if locked
        cur = db.cursor()
        sql = """SELECT Locked FROM Moving WHERE Direction = (%s) AND FromID = (%s)""" % (direction, location)
        cur.execute(sql)
        if cur.rowcount==1:
            for row in cur.fetchall():
                lock = row[0]
                if row[0]<4:
                    print ("It is locked. Lock level:",row[0],". Maybe there is a key somewhere?")
                    print (" ")
                else:
                    print (" ")
                    print("There is no lock on this side.")
                    print ("Maybe there is an another way to get this open?")
                    print (" ")
                destination = location
                return destination
        else:
                destination = location; # movement not possible
                print ("Invalid destination")
                return destination
            
def movementoptions(location):
    cur = db.cursor()
    sql = """SELECT direction, name FROM room JOIN moving on moving.toid = room.roomid WHERE moving.fromid = (%s) group by room.name order by moving.direction""" % (location)
    cur.execute(sql)
    for row in cur.fetchall():
        print (row[0]+". "+row[1])
        
    return   

def curloc(location):
    cur = db.cursor()
    sql = """Select name from room where roomid = (%s)""" % (location)
    cur.execute(sql)
    if cur.rowcount>=1:
        for row in cur.fetchall():
            details = row[0]
        return details

def look(location):
    cur = db.cursor()
    sql = """Select name from enemy where health_points<1 and enemy.roomid = (%s)""" % (location)
    cur.execute(sql)
    if cur.rowcount>=1:
        sql = """select details2 from room where roomid = (%s)""" % (location)
        cur.execute(sql)
        if cur.rowcount>=1:
            for row in cur.fetchall():
                details2 = row[0]
                return details2
    else:
        sql = """Select details from room where roomid = (%s)""" % (location)
        cur.execute(sql)
        if cur.rowcount>=1:
            for row in cur.fetchall():
                details = row[0]
                return details
    return

def lookat(location, target):
    if location == 2 and target == "map": #Special condition for opening map image file
        os.system('start gamemap.jpg') 
        print ("It's a map of the ships layout")
    elif target == 0:
        print ("What do you want to look at?")
    else:
        (description(location,target))

def items(location):
        cur = db.cursor()
        sql = """Select name from item_type join item on item_type.id = item.itemtypeid WHERE item.enemyid is NULL and item.roomid = %s""" % (location)
        cur.execute(sql)

        if cur.rowcount>0:
            print ("You see the following items:")
            print (" ")
            for row in cur.fetchall():
                print (row[0])
        else:
            print ("There are no items here")

def search(location):
    cur = db.cursor()
    sql = """Select item_type.name from enemy, item_type join item on item_type.id = item.itemtypeid WHERE item.enemyid is not null and enemy.health_points <1 and item.roomid = %s""" % (location)
    cur.execute(sql)
    if cur.rowcount>0:
        print ("You found the following items:")
        print (" ")
        for row in cur.fetchall():
           i = row[0]
    else:
           i = "There are no items here"
    return i
           

def kill(location):
    cur = db.cursor()
    sql = """UPDATE enemy SET enemy.health_points=0 WHERE enemy.roomid = %s""" % (location)
    cur.execute(sql)
    return

def enemyhp():
    cur = db.cursor()
    sql = """Select name,health_points from enemy"""
    cur.execute(sql)
    if cur.rowcount>0:
        print ("Enemy health list:")
        print (" ")
        i = cur.fetchall()
        print (i)
    else:
        print ("error")
    return


def pickup(location,playertarget):
    cur = db.cursor()
    sql = """Select item_type.name from item_type join item on item_type.id = item.itemtypeid join room on item.roomid= room.roomid WHERE room.roomid = %s AND item_type.name = "%s" """ % (location,playertarget)
    cur.execute(sql)
    if cur.rowcount>=1:
        for row in cur.fetchall():
            result = row[0]
            if result == playertarget:
                sql2 = """update item join item_type on item_type.id = item.itemtypeid set item.playerid = 1,
item.roomid = null where (item_type.name=("%s")) AND (item.roomid=("%s"))""" % (result,location)
                cur.execute(sql2)
                print ("You got",result)
            else:
                print ("You cannot pick that up")
                return
    else:
        print ("You cannot pick that up")
        return

def inventory():
    cur = db.cursor()
    sql = """select name from item_type join item on item_type.id = item.itemtypeid where item.playerid = 1 order by name"""
    cur.execute(sql)
    if cur.rowcount>0:
        for row in cur.fetchall():
            print (row[0])
    else:
        print("You don't have anything")

def usekeycard():
    cur = db.cursor()
    sql = "SELECT Id FROM item WHERE itemtypeid=7 AND item.playerid=1"
    cur.execute(sql)
    if cur.rowcount>=1:
        sql = "UPDATE moving SET Locked=0 WHERE locked=1"
        cur.execute(sql)
        if cur.rowcount>=1:
            print("All the lvl 1 doors are now unlocked.")
    else:
        print("You need a correct key.")
    return

def usekeycard2():
    cur = db.cursor()
    sql = "SELECT Id FROM item WHERE itemtypeid=11 AND item.playerid=1"
    cur.execute(sql)
    if cur.rowcount>=1:
        sql = "UPDATE moving SET Locked=0 WHERE locked=2"
        cur.execute(sql)
        if cur.rowcount>=1:
            print("All the lvl 2 doors are now unlocked.")
    else:
        print("You need a correct key.")
    return

def usekeycard3():
    cur = db.cursor()
    sql = "SELECT Id FROM item WHERE itemtypeid=12 AND item.playerid=1"
    cur.execute(sql)
    if cur.rowcount>=1:
        sql = "UPDATE moving SET Locked=0 WHERE locked=3"
        cur.execute(sql)
        if cur.rowcount>=1:
            print("All the lvl 3 doors are now unlocked.")
    else:
        print("You need a correct key.")
    return

def grenade(location):
    cur = db.cursor()
    sql = "SELECT Id FROM item WHERE itemtypeid=8 AND item.playerid=1"
    cur.execute(sql)
    if cur.rowcount>=1:
        if location == 7:
            sql = "UPDATE moving SET Locked=0 WHERE locked=4 and toid=11"
            cur.execute(sql)
            print("Door to the presidental suite is now open.")
        elif location == 8:
            location = "18"
            print (look(location))
            cur.execute('UPDATE playable_character SET health_points = 0')
    else:
        print("You shouldn't do that!")
    return


def help():
    print ("All commands must be lowercase")
    print (" ")
    print ("Type: 'look' to see the room description and the items in the room")
    print ("Type: 'look at X' to get detailed information. For example: 'look at window'")
    print ("Type: 'search' + 'body' to see the items the corpse is holding.")
    print (" ")
    print ("Type: 'move' to get all the possible movement options")
    print ("Select a direction by typing the corresponding number")
    print ("Type: 'use key' near a lock to open locks, there are multiple levels of locks")
    print (" ")
    print ("Type: 'pick' or 'pick up' + 'item name' to take the item. For example: 'pick up apple'")
    print ("Type: 'inventory' to see the items you're holding")
    print (" ")
    print ("Type: 'hp' to see your current health")
    print ("If you have a medkit: ")
    print ("Type: 'use medkit' to increase your health by 4 or until at max health")
    print (" ")
    print ("Hint: Grenade can also be a type of key")
    print (" ")
    print (" ")
    print ("Type: 'exit' to end the game")
    print (" ")
    print ("Type: 'restart' to restart the game")
    print (" ")
    return

def curhealth():
    cur = db.cursor()
    cur.execute('select health_points from playable_character')
    for row in cur.fetchall():
        i = row[0]
        print ('Your current health is:', row[0],'/ 10')
    return

def hurt():
    cur = db.cursor()
    cur.execute('select health_points from playable_character')
    results = cur.fetchall()
    for row in results:
        hp = row[0] - 4
        cur.execute('UPDATE playable_character SET health_points = (%s)' % (hp))
    cur.execute('select health_points from playable_character')
    for row in cur.fetchall():
        print('Your health is now:', row[0],'/ 10')
    return

def addkit():
    cur = db.cursor()
    cur.execute("UPDATE item SET playerid=1 WHERE item.ItemTypeID=4")
    return
    
def medkit():
    cur = db.cursor()
    cur.execute("SELECT Id FROM item WHERE itemtypeid=4 AND item.playerid=1")
    if cur.rowcount>=1:
        cur.execute('select health_points from playable_character')
        for row in cur.fetchall():
            i = row[0]

        if i==10:
            print("You're already on full HP")

        elif i<=6:
            cur.execute('select health_points from playable_character')
            results = cur.fetchall()
            for row in results:
                hp = row[0] + 4
                cur.execute('UPDATE playable_character SET health_points = (%s)' % (hp))
            cur.execute('select health_points from playable_character')
            for row in cur.fetchall():
                print('Your health is now:', row[0],'/ 10')
            cur.execute('UPDATE item SET playerid = NULL WHERE item.ItemTypeID=4')


        elif i<10 and i>6:
            cur.execute('select health_points from playable_character')
            results = cur.fetchall()
            cur.execute('UPDATE playable_character SET health_points = 10')     
            cur.execute('select health_points from playable_character')
            for row in cur.fetchall():
                print('Your health is now:', row[0],'/ 10')
            cur.execute('UPDATE item SET playerid = NULL WHERE item.ItemTypeID=4')

        
        else:
            print("Error")
         
    else:
        print("You don't have a medkit")           
    return

def counter():
    cur = db.cursor()
    cur.execute("UPDATE Playable_character SET Time_current = Time_current + 1")

def movecounter():
    cur = db.cursor()
    cur.execute("select Time_current FROM Playable_character")
    for row in cur.fetchall():
        print(row[0])

def energy(location):
    cur = db.cursor()
    cur.execute("UPDATE Playable_character SET Time_current = Time_current - 6")
    sql ="""UPDATE item SET item.RoomId = NULL where item.roomid = %s""" % (location)
    cur.execute(sql)
        
#Main program
location = "1"
leave = 0
done = 0

# Clear console
print("\n"*1000)

# Begining prints
print("""
     _______..______      ___       ______  _______         
    /       ||   _  \    /   \     /      ||   ____|        
   |   (----`|  |_)  |  /  ^  \   |  ,----'|  |__    ______ 
    \   \    |   ___/  /  /_\  \  |  |     |   __|  |______|
.----)   |   |  |     /  _____  \ |  `----.|  |____         
|_______/    | _|    /__/     \__\ \______||_______|        
                                                            
  ______ .______       __    __   __       _______. _______ 
 /      ||   _  \     |  |  |  | |  |     /       ||   ____|
|  ,----'|  |_)  |    |  |  |  | |  |    |   (----`|  |__   
|  |     |      /     |  |  |  | |  |     \   \    |   __|  
|  `----.|  |\  \----.|  `--'  | |  | .----)   |   |  |____ 
 \______|| _| `._____| \______/  |__| |_______/    |_______|

""")
print(" ")
print(" ")
print(" ")
print("----- Type 'help' for Command list -----")
print(" ")
print(" ")
print(" ")
print("You wake up in a public bathroom. ")
print(" ")

while leave !=1:
    playersubcmd = 0 #Reset action 2
    playertarget = 0 #Reset target
    while True:
        try:
            playerinput = input("What do you want to do?: ")
            playerinput = playerinput.split()
            playercmd = playerinput[0] #Action (1st word of input)
            break
        except IndexError: #Sometimes code starts reading list before input. This forces the input. Roughly 10% chance of error.
            print ("Input a command")
            
    if len(playerinput) ==2:
        playersubcmd = playerinput[1] #Define action 2 (2nd word of input)
    if len(playerinput)>2:
        playersubcmd = playerinput[1]
        playertarget = playerinput[2] #Define target (3rd word of input "Look at x")
    print("")
    
    
    if playercmd =="look" or playersubcmd == "look": #Look around
        if playersubcmd == "at":
            (lookat(location,playertarget))
        else:
            print(look(location))
            (items(location))
            counter()
       
    elif playercmd == "search" or playercmd == "investigate" and playersubcmd == "body" or playersubcmd == "corpse":
        print(search(location))
        counter()

    elif playercmd == "move" or playersubcmd == "move": #Movement
        print (" ")
        print ("Your current location is",curloc(location))
        print ("Available locations")
        movementoptions(location)
        while True:
            try:
                direction = (int(input("Input direction: ")))
                break
            except ValueError: #Force int input
                print ("Input a number")
        
        print (" ")
        location = movement(location,direction)
        print (look(location))
        counter()
        
    elif playercmd == "pick" or playersubcmd == "pick": #Pick up items
        if playertarget == "energydrink":
            energy()
            print ("You pick up and consume the energy drink")
            print(" ")
            print("Is time slowing down or am I just moving faster...?")
            print(" ")
        else:
            pickup(location, playertarget)
            counter()

    elif playercmd=="use":    # use
        if playersubcmd=="":
            print("I don't know what to use.")
        elif location==2 and playersubcmd=="key" or location==2 and playersubcmd=="keycard":
            usekeycard();
            counter()
        elif location==7 and playersubcmd=="key" or location==7 and playersubcmd=="keycard":
            usekeycard2();
            counter()
        elif location==17 and playersubcmd=="key" or location==17 and playersubcmd=="keycard":
            usekeycard3();
            counter()
        elif location==7 and playersubcmd=="grenade" or location==8 and playersubcmd=="grenade":
            grenade(location);
            counter()
        elif playersubcmd=="medkit":
            medkit();
            counter()
        else:
            print("You can't do that.")
        
    elif playercmd == "help" or playersubcmd == "help": #Help
        help()
        
    elif playercmd == "exit" or playersubcmd == "exit": #Exit
        leave = 1
        db.rollback()
        counter()
        
    elif playercmd == "current health" or playercmd == "health" or playercmd == "hp": #Current health
        curhealth()
        counter()

    elif playercmd == "enemyhp": #kill results
        enemyhp()
        counter()

    elif playercmd == "counter": #number of moves made
        movecounter()

        
    elif playercmd == "inventory" or playersubcmd == "inventory": #Show held items
        inventory()
        checkammo()
        counter()
        
    elif playercmd == "suicide" or playersubcmd == "suicide" and location == 1:
        print ("You start to choke yourself and pass out.")
        print (" ")
        print (" ")
        print (" ")
        print (" ")
        print (" ")
        print (look(location))
        counter()
    else: #Invalid command
        print ("Please input a valid command, type 'help' for instructions")    
    # Dying 
    cur = db.cursor()
    cur.execute('select health_points, Time_current, Time_max FROM Playable_character')
    for row in cur.fetchall():
        i = row[0]
        a = row[1]
        b = row[2]
    if i<=0:
        print("You died!!")
        leave = 1
    elif a>=b:
        leave = 1
        print(" ")
        print("You ran out of time, the ship is in the stars orbit and escaping is too late")
        print(" ")
        print("Game over!!")

    print (" ")


    if location==13 and done !=1:
        
        leave = checkhelmet()
        done = 1

    if leave !=1:
        if location ==11 or location == 13 or location == 14 or location == 15 or location == 16 or location == 17:
            if enemycheck()>=1:
               location = combat()
               leave = playercheck()
    if location == 19:
        print("Game over!!")
        print(" ")
        print ("-----You had",movecounter(),"actions remaining, well done!-----")
        print(" ")
        input("Want to play again? (y/n): ")
        if input == "y":
            db.rollback()
            location = "1"
        else:
            leave = 1
            print("Good bye!")
