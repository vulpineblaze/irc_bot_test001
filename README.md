# irc_bot_test001
gonna experiment with making a game-focused irc bot



## Description:

This is an irc based idle-quest minigame bot. 

## Install Instructions:

// need to describe how to get a bot work for someone else

______________________________________________________


## Design Doc: 

#### Current Version is:    __**1.0.1**__


### Command List:

// need to put current command list and re-iterate version here

### Design Goals:

Simple is better than complex. Complex is better than complicated.

I'd rather have a simple front end and a complex back end, than a simple backend and a complicated fromt end. 

The fewer unique commands the better. The fewer nested commands the more-better; OR better yet, not at all.  

Joke-Theme: Make enough of the text configurable such that this game could be MLP themed. 


_________________________________

#### Function Requirements:    *--Version 1.0.1*


  * Players will be inducted into the database upon joining the channel.
  * Players may attack other players in the channel

  * Stats are as follows:   *--Version 1.0.1*
    * attack , int , starts at 1
    * defense , int , starts at 1
    * health , int , starts at 100

  * Fighting algorithm now:      *--Version 1.0.1*
    * max( 1, Ad6 - Dd6 ) , where A and D are attack and defense
    * so A of 5 and D of 6 would become  5d6 - 6d6  , or  (5 to 30)  minus (6 to 36)

  * Death can occur, but isnt implemented     *--Version 1.0.1*

  * health exists, but there is no way to regenerate it   *--Version 1.0.1*

  * admin command only does reload right now   *--Version 1.0.1*

___________________________________________

#### Function Requirements:    *Version 1.1.0*

  * Players will be inducted into the database upon joining the channel.    *--Version 1.0.1*
  * Players may attack other players in the channel     *--Version 1.0.1*
    * Monsters will be separate bots, not in this code base

  * Players earn juice for winning fights

  * Players may increase their stats 
    * cost in juice to initiate timer
    * timedelta = (lvl)^2.8 in seconds
      * at lvl 13, increasing a stat will take 21 minutes

  * Stats could become:   
    * attack - int, starts at 1
      * purchased
    * defense - int, starts at 1
      * purchased
    * crit - int, starts at 1
      * purchased
    * level - int, starts at 1
      * anytime any other stat is purchased, this increments too
      * juice cost to level anything = lvl*stat
    * health - int, starts at *(doesnt matter, non-zero default val)*
      * replaced by lvl\*2 + defense\*2 + 20 
      * cost to rez = lvl*(defense) + health
      * current health is stored is db, max health is calculated when needed
        * if effect makes current health > max health, then current health = max health. duh. 
    * juice
      * combo of gold and XP, reward for fighting
      * juice = max(1, 2 \* (enemy.lvl - 0.9\*your.lvl) )
        * juice = min( juice, your.lvl*2 )
        * you cant get more juice from a kill than double your current level
      * juice issued to Player upon enemy death, last hit
      * rename-able stat? all stats renameable?

  * Fighting algorithm could be:  
    * max(1 , A + C - D)
    * C = max(0, (crit\*3)d6 - (crit\*3)d6) 
      * slight chance of doing additional x3 damage

  * Equipment might be cool, but there are no plans to implement
    * Complicates everything. Might prefer this to be flavor-text only.
    * attack + "My massive enhanced rocket-powered flaming mini-nuke mjornir of burninateing does 1 damage..."

  * skills might be cool, but no plan to implement
    * same as equipment, only worse.
    * could be limited to effect + flavor-text
    * attack + "I cast lvl.99999999 Magic Missile for 1 damage...", now you have spells
    * heal as negative attack? temporary stat-boost skill? 

  * Death can occur, but isnt implemented      *Version 1.0.1*
    * dead Players should'nt be able to attack, be victim, level up, etc..
      * make sure dying is un-fun, something to be avoided

    * need a way to revive, continue playing
      * rez one per hour/day/week ?
      * command-based cost? auto-deduct gold? loss of xp, levels, stats?

  * health exists, but there is no way to regenerate it   *--Version 1.0.1*
    * free potions? find potions? buy potions?
    * free health every hour/day/week?
      * command based on timer, or passive

    * combat healing skill? cost mana? gold? xp?  

  * health vs dying
    * dying is not just 0 health, you have to un-do the death
    * avoid dying; more than just "oh my health is low, lawl whatev"
    * ultra-high chars should be significantly more expensive to rez


  * admin command only does reload right now   *--Version 1.0.1*
    * should be able to manipulate any part of any Players anything
    * maybe even change say_hi and good_bye messages?
    * die command? 

  * monster commands
    * monster bots will need access to specialized admin-esque commands, to respawn and whatnot
    * implement a new command, `!monster` , check is_monster flag, hide from `!help` list


  * **attacks, defends, and other actions may be madlib'able by each player**
    * eg. : 
      * `!q setname bloodninja`
      * `!q setattack casts lvl.9999999 lightning bolt`
      * `!q setdefend I put on my hat and wizard robe`
    * make a "profile" db object, store all of the madlib text
    * this opens up the option of having bots act as 'Player' to create monsters, saves a shitton of coding and complexity in this project
      * second project would be config-driven bot Monsters, might need is_monster flag in this project though for some logic

  * madlib events:
    * attack
      * <Player> <does_attack> to <Victim> who <does_defend> for X <damage> <if_die_message>
    * crit > attack
      * <Player> <does_crit> for X <damage>  
        * leave off defend text?
    * defend
      * covered in attack
    * die
      * covered in attack
    * heal
      * <Player> <does_heal> for X <health>
    * rez
      * <Player> <does_rez>
  * madlib, new word for each stats / effect:
    * attack
      * Increase <attack> for X <juice>? Will take X seconds|minutes|hours|days.
      * stats: <attack>:X | <defense>:Y | <crit>:Z | ...
        * or keep both?
        * stats: attack:"<attack>":X | defense:"<defense>":Y | crit:"<crit>":Z | ...
        * or keep original in stats, and have separate prfile viewer?
        * stats: attack:X | defense:Y | crit:Z | ...
    * defense
    * crit
    * level
    * health
    * damage
    * heal
    * rez
    * juice

##### Equations:

item|#|#|#|#|#|#|#|#|#|#
---|---|---|---|---|---|---|---|---|---|---
attack|1|2|5|10|20|50|100|20|20|60
defense|1|2|5|10|20|50|100|20|60|20
crit|1|2|5|10|20|50|100|60|20|20
health|24|32|56|96|176|416|816|256|336|256
level|1|4|13|28|58|148|298|98|98|98
||||||||||
cost to rez|25|40|121|376|1336|7816|30616|2216|6216|2216
max damage no crit|0|0|0|0|0|0|0|0|-240|240
max damage high def|0.15|0.3|0.75|1.5|3|7.5|15|9|-237|243
max damage wo def|20|40|100|200|400|1000|2000|1000|360|640
max damage|15|30|75|150|300|750|1500|900|60|540
max crit|15|30|75|150|300|750|1500|900|300|300
||||||||||
time modifier|2.8|||||||||
first level in seconds|1|48.50293013|1315.350174|11273.07737|86616.0515|1193253.737|8468481.428|376212.3187|376212.3187|376212.3187
minutes|0.016666667|0.808382169|21.92250289|187.8846229|1443.600858|19887.56228|141141.3571|6270.205311|6270.205311|6270.205311
hours|0.000277778|0.013473036|0.365375048|3.131410381|24.0600143|331.4593714|2352.355952|104.5034218|104.5034218|104.5034218
days|1.15741E-05|0.000561377|0.01522396|0.130475433|1.002500596|13.81080714|98.01483134|4.354309244|4.354309244|4.354309244
||||||||||
your.lvl|1|2|5|2|10|20|20|50|100|100
enemy.lvl|1|2|2|5|20|10|20|100|50|100
juice|1|1|1|6.4|22|1|4|110|1|20



