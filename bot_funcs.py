
import bot_db
from random import randint
# print(randint(0,9))


User = bot_db.User

THE_CHANNEL="#wtfomfg"

def roll_many_dice(number):
    ret_val = 0
    for i in xrange(number):
        ret_val += randint(1,6)
    return ret_val



class func(object):
    def __init__(self, bot, db):
        self.bot = bot 
    def test(self, target, msg):
        self.bot.privmsg(target, msg)

    def toggle_active(self, nick, is_active):
            user = self.get_or_create_user(nick)
            user.is_active=is_active
            user.save()
            self.bot.privmsg(THE_CHANNEL, "toggled nick: "+nick+", to: "+str(user.is_active))


    def get_or_create_user(self, nick): 
        # self.bot.privmsg(target, msg)grandma = Person.get(Person.name == 'Grandma L.')
        try:  
            temp = User.get(User.username == nick)
            self.bot.privmsg("THE_CHANNEL", "found nick: "+nick)
        except: 
            temp = User.create(username=nick, attack=1, defense=1, health=100)
            self.bot.privmsg(THE_CHANNEL, "created nick: "+nick)
            temp.save

        return temp


    def parse_victim(self, rcvd):
        s2 = "attack"
        victim = rcvd[rcvd.index(s2) +1+ len(s2):]
        return victim

    def validate_victim(self, victim):
        ret_val = "dummy"
        try:  
            temp = User.get(User.username == victim)
            # self.bot.privmsg(THE_CHANNEL, "found victim: "+victim)
            if temp.is_active:
                ret_val = victim
        except: 
            pass
            # self.bot.privmsg(THE_CHANNEL, "no such victim: "+victim+", using dummy.")

        if ret_val is "dummy":
            self.bot.privmsg(THE_CHANNEL, "no such victim: "+victim+", using dummy.")
        else:
            self.bot.privmsg(THE_CHANNEL, "found victim: "+victim)

        return ret_val

    def do_battle(self, user, victim):
        battle_msg = ""
        try:  
            temp = User.get(User.username == victim)
        except: 
            #probably dummy
            temp = User.create(username=victim, attack=1, defense=1, health=100)

        damage = roll_many_dice(user.attack) - roll_many_dice(temp.defense)
        if damage < 1:
            damage = 1

        battle_msg += user.username +" has "+str(user.attack)+" attack against "+temp.username+"'s defense of " +str(temp.defense)

        temp.health -= damage
        if temp.health < 0:
            temp.health = 0;
            # self.bot.privmsg("#wtfomfg", "no such victim: "+victim+", using dummy.")
            battle_msg += " and kills them."
        else:
            battle_msg += " and wounds them for "+str(damage)+" point of damage."


        temp.save()

        return battle_msg


        # self.bot.privmsg("#wtfomfg", "found user: "+user)
        # if not temp:
        #     temp = User.create(username=user)
        #     self.bot.privmsg("#wtfomfg", "created user: "+user)
        #     temp.save
        # return temp



# class user(object):
#     def __init__(self, bot, db):
#         self.db = db 
#         self.bot = bot 
#     def test(self, target, msg):
#         self.bot.privmsg(target, msg)

