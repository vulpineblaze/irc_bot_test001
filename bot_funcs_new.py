
import bot_db
from random import randint
import datetime.datetime as datetime
import datetime.timedelta as timedelta

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
        self.is_debug = Admin.get(version=self.bot.version).is_debug
    def test(self, target, msg):
        self.bot.privmsg(target, msg)

    def set_target(self, target):
        self.target = target

    def toggle_active(self, nick, is_active):
        user = self.get_or_create_user(nick)
        user.is_active=is_active
        user.save()
        if self.is_debug:
            self.bot.privmsg(self.target, "toggled nick: "+nick+", to: "+str(user.is_active))

    def toggle_debug(self, is_debug):
        admin = Admin.get(version=self.bot.version)
        admin.is_debug = is_debug
        admin.save()

    def calc_juice(self, user, vic):
        juice = 2 * (vic.level - 0.9 * user.level)
        if juice < 1:
            juice = 1
        return juice

    def find_max_health(self, user):
        max_health = user.level*2 + user.defense*2 + 20
        return max_health

    def find_rez_cost(self, user):
        max_health = self.find_max_health(user)
        cost = user.level*user.defense + max_health
        return cost

    def find_level_cost(self, user, stat):
        cost = user.level*stat
        return cost

    def find_training_time_seconds(self, user):
        seconds = user.level ^ 2.8
        return seconds

    def find_training_time(self, user):
        seconds = find_training_time_seconds(user)
        datetime = datetime.now() + timedelta(seconds=seconds)
        return datetime

    def check_if_dead(self, user):
        ret_bool = False
        if user.health == 0:
            ret_bool = True
        return ret_bool

    def get_or_create_user(self, nick): 
        # self.bot.privmsg(target, msg)grandma = Person.get(Person.name == 'Grandma L.')
        try:  
            temp = User.get(User.username == nick)
            if self.is_debug:
                self.bot.privmsg(self.target, "found nick: "+nick)
        except: 
            temp = User.create(username=nick, 
                                attack=1, 
                                defense=1, 
                                crit=1, 
                                level=1, 
                                juice=1, 
                                health=100, 
                                is_active=True)
            if self.is_debug:
                self.bot.privmsg(self.target, "created nick: "+nick)
            temp.save

        return temp


    def parse_victim(self, rcvd):
        s2 = "attack"
        victim = rcvd[rcvd.index(s2) +1+ len(s2):]
        return victim

    def validate_victim(self, victim):
        ret_val = "dummy"
        try:  
            vic = User.get(User.username == victim)
            # self.bot.privmsg(self.target, "found victim: "+victim)
            if vic.is_active:
                ret_val = victim
        except: 
            pass
            # self.bot.privmsg(self.target, "no such victim: "+victim+", using dummy.")

        if ret_val is "dummy":
            self.bot.privmsg(self.target, "no such victim: "+victim+", using dummy.")
        elif self.check_if_dead(vic):
            self.bot.privmsg(self.target, victim+" is dead, using dummy.")
        else:
            if self.is_debug:
                self.bot.privmsg(self.target, "found victim: "+victim)

        return ret_val

    def do_battle(self, user, victim):
        battle_msg = ""
        vic = self.get_or_create_user(victim)

        crit = roll_many_dice(3*user.crit) - roll_many_dice(3*user.crit)
        if crit < 0:
            crit = 0

        damage = roll_many_dice(user.attack) + crit - roll_many_dice(vic.defense)
        if damage < 1:
            damage = 1

        battle_msg += user.username +" has "+str(user.attack)+" attack against "+vic.username+"'s defense of " +str(vic.defense)

        vic.health -= damage
        if vic.health < 0:
            vic.health = 0;
            # self.bot.privmsg("#wtfomfg", "no such victim: "+victim+", using dummy.")
            user.juice = calc_juice(user, vic)
            user.save()
            battle_msg += " and kills them."
        else:
            battle_msg += " and wounds them for "+str(damage)+" point of damage."


        vic.save()

        return battle_msg

    def heal(self, user):
        max_health = self.find_max_health(user)
        missing_health = max_health - user.health

        out_msg = ""

        if missing_health == 0:
            out_msg = "You are at full health."
        elif user.juice < missing_health:
            new_miss_health = user.juice
            out_msg = "You only have "+new_miss_health+" juice, and so you'll only get that much health."
            user.juice = 0
            user.health += new_miss_health
            user.save()
        # elif:
        #     pass
        else:
            out_msg = "Now healing "+missing_health+" health."
            user.juice -= missing_health
            user.health += missing_health
            user.save()

        return out_msg


    def rez(self, user):
        max_health = self.find_max_health(user)
        out_msg = ""
        cost = find_rez_cost(user)
        if self.check_if_dead(user):
            out_msg = "You are not dead."
            return out_msg

        if (datetime.now() - user.last_rez).days > 1:  
            out_msg = "You are using your one free rez today!"
            user.last_rez = datetime.now()
            user.health = max_health
            user.save()
        elif user.juice < cost:
            out_msg = "You can't afford to rez."
        else:
            out_msg = "You got rez'd!"
            user.juice -= cost
            user.health = max_health
            user.save()

        return out_msg


    def print_stats(self, user):
        prof = user.profile
        out_msg = "Your profile is: "+prof.alt_username
        out_msg += "\n | attack:"+prof.attack+":"+str(user.attack)
        out_msg += "\n | defense:"+prof.defense+":"+str(user.defense)
        out_msg += "\n | crit:"+prof.crit+":"+str(user.crit)
        out_msg += "\n | level:"+prof.level+":"+str(user.level)
        out_msg += "\n | juice:"+prof.juice+":"+str(user.juice)
        out_msg += "\n | health:"+prof.health+":"+str(user.health)
        out_msg += "\n | last_rez:"+str(user.last_rez)
        out_msg += "\n | finish_training:"+str(user.finish_training)
        out_msg += "\n "

        return out_msg


    def train_stat(self, user, stat):

        if user.finish_training - datetime.now() > 0:
            out_msg = "You cannot train until: "+str(user.finish_training)
            return out_msg

        if user.finish_training - datetime.now() > 0:
            out_msg = "You cannot train until: "+str(user.finish_training)
            return out_msg
        
        if stat == "attack":
            num_stat = user.attack
        elif stat == "defense":
            num_stat = user.defense
        elif stat == "crit":
            num_stat = user.crit
        else:
            out_msg = "Stat: "+str(num_stat)+" not recognized. This msg should never happen!"
            return out_msg

        cost = find_level_cost(user, num_stat)
        if user.juice < cost:
            out_msg = "You don't have enough juice to level. Has: "+str(user.juice)+" Need:"+str(cost)
            return out_msg

        if stat == "attack":
            user.attack += 1
        elif stat == "defense":
            user.defense += 1
        elif stat == "crit":
            user.crit += 1
        else:
            out_msg = "Stat: "+str(num_stat)+" not recognized. This msg should never happen!"
            return out_msg

        user.juice -= cost
        user.level += 1
        user.health = find_max_health(user)
        num_stat += 1

        out_msg = "Spent "+str(cost)+" juice and increased "+stat+" to "+num_stat
        # seconds = level
        user.finish_training = find_training_time(user)

        user.save()

        return out_msg


#         now = datetime.datetime.now()
# now_plus_10 = now + datetime.timedelta(minutes = 10)