# -*- coding: utf-8 -*-
from irc3.plugins.command import command
import irc3
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

import bot_funcs as ex_func
import bot_db

db = bot_db.db

# db.create_tables([User, Tweet])



@irc3.plugin
class Plugin(object):

    def __init__(self, bot):
        self.bot = bot
        self.func = ex_func.func(bot, db)

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

    # @command
    # def reload(self, mask, target, args={'<words>':'Reload!'}):
    #     """Reload command

    #         %%reloads the bot
    #     """
    #     self.bot.reload('mybot_plugin')
    #     self.bot.privmsg(target, "You sent in: "+' '.join(args['<words>']))

    # @command(permission='view')
    # def echo(self, mask, target, args):
    #     """Echo

    #         %%echo <message>...
    #     """
    #     yield ' '.join(args['<message>'])

    # @command
    # def ec(self, mask, target, args):
    #     """Ec command
    #         %%ec <words>...
    #     """ 
    #     # self.func.test(target, "You sent in: "+' '.join(args['<words>']))
    #     msg = ""
    #     # msg += " mask : ".join(mask)
    #     # msg += " target : ".join(target)
    #     msg += " words : ".join(args['<words>'])
    #     self.func.test(target, msg)
    # #     self.bot.reload('mybot_plugin')
    #     # self.bot.privmsg(target, "You sent in: "+' '.join(args['<words>']))


    @command(permission='admin')
    def admin(self, mask, target, args):
        """Admin command
            %%admin <words>...
        """ 
        rcvd = ' '.join(args['<words>'])
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
            self.func = ex_func.func(the_bot, db)
            self.bot.reload('mybot_plugin')
        elif rcvd == "debug_on":
            self.func.toggle_debug(True)
        elif rcvd == "debug_off":
            self.func.toggle_debug(False)
        else:
            self.bot.privmsg(target, "I dont recognize: "+rcvd)

    @command(permission='admin', public=False)
    def admin_edit(self, mask, target, args):
        """Admin_edit command
            %%admin_edit <words>...
        """ 
        rcvd = ' '.join(args['<words>'])

        if not target:
            target = mask.nick
        if target == self.bot.nick:
            target = mask.nick

        if self.is_debug:
            msg = " Command received : " + rcvd + ", from: "+target
            self.bot.privmsg(target, msg)

        self.bot.privmsg(target, "testing: "+str(args[0]))







    @command
    def q(self, mask, target, args):
        """Q command
            %%q <words>...
            stats - Prints the stats of your character
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

        if rcvd == "stats":
            msg = self.func.print_stats(user)
            self.bot.privmsg(mask.nick, msg)

        elif "attack" in rcvd:
            if self.func.check_if_dead(user):
                battle_msg = user.username+" is dead and can not attack anyone."
            else:
                victim = self.func.parse_victim(rcvd)
                victim = self.func.validate_victim(victim)
                battle_msg = self.func.do_battle(user, victim)
            # msg += user.username + " attacks " + victim + " for Zero damage cuz devbuild. "
            self.bot.privmsg(target, battle_msg)

        elif "version" in rcvd:
            self.bot.privmsg(target, "Version is: "+VERSION)

        elif "heal" in rcvd:
            msg = self.func.heal(user)
            self.bot.privmsg(mask.nick, msg)

        elif "rez" in rcvd:
            msg = self.func.rez(user)
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
            stats - Prints the stats of your character
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
