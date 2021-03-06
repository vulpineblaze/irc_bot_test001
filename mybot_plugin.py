# -*- coding: utf-8 -*-
from irc3.plugins.command import command
import irc3
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

import bot_funcs as ex_func
import bot_db

db = bot_db.db
Admin = bot_db.Admin
# db.create_tables([User, Tweet])


VERSION = "1.1.0"


@irc3.plugin
class Plugin(object):

    def __init__(self, bot):
        self.bot = bot
        try:
            self.is_debug = Admin.get(version=VERSION).is_debug
        except:
            self.is_debug = Admin.create(version=VERSION).is_debug
        self.func = ex_func.func(bot, db, VERSION, self.is_debug)
        self.func.version = self.version = VERSION

    @irc3.event(irc3.rfc.JOIN)
    def say_hi(self, mask, channel, **kw):
        """Say hi when someone join a channel"""
        msg = ""
        if mask.nick != self.bot.nick:
            msg += 'Hi %s!' % mask.nick
            self.func.toggle_active(mask.nick, True)
        else:
            msg+='Hi!'
        self.bot.privmsg(channel, msg+' I\'m a mini-game! Use  !help  to see my available commands.')

    @irc3.event(irc3.rfc.QUIT)
    def good_bye(self, mask, **kw):
        """Say good bye when someone leaves a channel"""
        msg = ""
        channel="#wtfomfg"
        if mask.nick != self.bot.nick:
            msg += 'Bye %s!' % mask.nick
            self.func.toggle_active(mask.nick, False)
        else:
            msg+='Bye!'
        self.bot.privmsg(channel, msg+" I\'ll miss you.")


    @command(permission='admin')
    def admin(self, mask, target, args):
        """Admin command
            %%admin <words>...
            reload - reloads the bot without restarting
            debug_on - toggle debug text to appear
            debug_off - toggle debug text suppression
        """ 
        rcvd = ' '.join(args['<words>'])
        self.func.set_target(target)

        if not target:
            target = mask.nick
        if target == self.bot.nick:
            target = mask.nick
        if self.is_debug:
            msg = " Command received : " + rcvd + ", from: "+target
            self.bot.privmsg(target, msg)
        if rcvd == "reload":
            self.bot.privmsg(mask.nick, " ... Will now reload the bot!")
            the_bot = self.bot
            temp = reload(ex_func)
            self.func = ex_func.func(the_bot, db, VERSION,self.is_debug)
            self.func.set_target(target)
            self.bot.reload('mybot_plugin')
        elif rcvd == "debug_on":
            self.func.toggle_debug(True)
            self.is_debug = True
        elif rcvd == "debug_off":
            self.func.toggle_debug(False)
            self.is_debug = False
        else:
            self.bot.privmsg(target, "I dont recognize: "+rcvd)

    @command(permission='admin', public=False)
    def admin_edit(self, mask, target, args):
        """Admin_edit command
            %%admin_edit <words>...
            user NAME stat STAT AMOUNT - where caps are the target Player and stat to set to amount
            --eg. user jg stat juice 999999
        """ 
        rcvd = ' '.join(args['<words>'])
        self.func.set_target(target)

        if not target:
            target = mask.nick
        if target == self.bot.nick:
            target = mask.nick

        if self.is_debug:
            msg = " Command received : " + rcvd + ", from: "+target
            self.bot.privmsg(target, msg)

        # self.bot.privmsg(target, "testing: "+str(args['<words>'][0]))
        # for val in args['<words>']:
        #     self.bot.privmsg(target, val)
        user = "fake"
        stat = "fake"
        amount = -1
        create = "fake"

        for idx, val in enumerate(args['<words>']):
            if self.is_debug:
                self.bot.privmsg(target, "idx: "+str(idx)+", val: "+val)
            # if val == "stat":
                # self.bot.privmsg(target, "args['<words>']+1: "+args['<words>'][idx+1])
            if val == "user":
                user = args['<words>'][idx+1]
            elif val == "stat":
                stat = args['<words>'][idx+1]
                amount = args['<words>'][idx+2]
            elif val == "create": 
                create = "create"
            else:
                pass

        if (user != "fake") and (stat != "fake") and (amount != -1):
            temp = self.func.get_or_create_user(user)
            try:
                setattr(temp, stat, int(amount))
                temp.save()
                msg = "Admin set user: "+user+", stat: "+stat+", amount:"+str(amount)
                self.bot.privmsg(user, msg)
            except:
                self.bot.privmsg(target, "ERROR: failed setattr("+user+","+stat+","+str(amount)+")")
        elif (user != "fake") and (create != "fake"):
            temp = self.func.get_or_create_user(user)
            msg = "Created user: "+user
            if self.is_debug:
                self.bot.privmsg(target, "DEBUG: "+mask.nick+": "+msg)
            self.bot.privmsg(mask.nick, msg)
        else:
            msg = " Command malformed : " + rcvd + ", from: "+target
            msg += "\n user: "+user+", stat: "+stat+", amount:"+str(amount)
            self.bot.privmsg(target, msg)








    @command
    def q(self, mask, target, args):
        """Q command
            %%q <words>...
            stats - Prints the stats of your character
            attack VICTIM - you will attack the Player 
            version - Prints the program version
            heal - Heals your character, costs juice = hp healed
            rez - revives your dead char. One free/day, then it costs juice
        """ 
        msg = ""

        self.func.set_target(target) # target should be chan
        
        user = self.func.get_or_create_user(mask.nick)
        self.func.validate_health(user)

        if not user.is_active:
            user.is_active=True
            user.save()

        rcvd = ' '.join(args['<words>'])

        if rcvd == "stats":
            msg = self.func.print_stats(user)
            if self.is_debug:
                self.bot.privmsg(target, "DEBUG: "+mask.nick+": "+msg)
            self.bot.privmsg(mask.nick, msg)

        elif "attack" in rcvd:
            if self.func.check_if_dead(user):
                battle_msg = user.username+" is dead and can not attack anyone."
            else:
                victim = self.func.parse_victim(rcvd)
                victim = self.func.validate_victim(victim)
                battle_msg = self.func.do_battle(user, victim)
            # msg += user.username + " attacks " + victim + " for Zero damage cuz devbuild. "
            if target != mask.nick:
                self.bot.privmsg(mask.nick, battle_msg)
            
            self.bot.privmsg(target, battle_msg)
            self.bot.privmsg(victim, battle_msg)

        elif "version" in rcvd:
            self.bot.privmsg(target, "Version is: "+VERSION)

        elif "heal" in rcvd:
            if self.func.check_if_dead(user):
                msg = user.username+" is dead and can not attack anyone."
            else:
                msg = self.func.heal(user)

            if self.is_debug:
                self.bot.privmsg(target, "DEBUG: "+mask.nick+": "+msg)
            self.bot.privmsg(mask.nick, msg)

        elif "rez" in rcvd:
            msg = self.func.rez(user)
            if self.is_debug:
                self.bot.privmsg(target, "DEBUG: "+mask.nick+": "+msg)
            self.bot.privmsg(mask.nick, msg)

        else:
            self.bot.privmsg(target, "I dont recognize: "+rcvd)
        # self.func.test(target, msg)
        # self.bot.reload('mybot_plugin')
        # self.bot.privmsg(target, "You sent in: "+' '.join(args['<words>']))




    @command
    def training(self, mask, target, args):
        """Training command
            %%training <words>...
            STAT - trains the STAT you want (attack, defense, or crit)
        """ 
        # self.func.test(target, "You sent in: "+' '.join(args['<words>']))
        msg = ""
        # msg += " mask : "+mask
        # msg += " mask.nick : "+mask.nick
        # msg += " target : "+target
        # msg += " words : ".join(args['<words>'])
        # msg += "\n"

        self.func.set_target(target) # target should be chan
        
        user = self.func.get_or_create_user(mask.nick)
        if not user.is_active:
            user.is_active=True
            user.save()

        rcvd = ' '.join(args['<words>'])

        if (rcvd == "attack") or (rcvd == "defense") or (rcvd == "crit"):
            msg = self.func.train_stat(user, rcvd)
            self.bot.privmsg(mask.nick, msg)

        else:
            self.bot.privmsg(target, "I dont recognize: "+rcvd)


    # @command
    # def testt(self, mask, target, args):
    #     # self.func.test(target, "You sent in: "+' '.join(args['<words>']))
    #     msg = ""
    #     # msg += " mask : ".join(mask)
    #     # msg += " target : ".join(target)
    #     msg += " words : ".join(args['<words>'])
    #     self.func.test(target, msg)
