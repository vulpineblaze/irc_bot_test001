# irc_bot_test001
gonna experiment with making a game-focused irc bot


## Design Doc: 

### Description:

This is an irc based idle-quest minigame bot. 

#### Design Goals:

Simple is better than complex. Complex is better than complicated.

I'd rather have a simple front end and a complex back end, than a simple backend and a complicated fromt end. 

The fewer unique commands the better. The fewer nested commands the more-better; OR better yet, not at all.  

Joke-Theme: Make enough of the text configurable such that this game could be MLP themed. 

#### Function Requirements:  *(kinda)*


  * Players will be inducted into the database upon joining the channel.
  * Players may attack other players in the channel
    * Monsters will be separate bots, not in this code base

  * Players earn ?gold? for winning fights
    * Spend gold on what?

  * Players may increase their stats 
    * I want it to be timer-based, where the first stat is very quick, and additional stat increases take longer and longer. 
    * may also be XP based, must spend XP to initiate the timer?

  * attacks, defends, and other actions may be madlib'able by each player
    * eg. : 
      * `!q setname bloodninja`
      * `!q setattack casts lvl.9999999 lightning bolt`
      * `!q setdefend I put on my hat and wizard robe`

    * this opens up the option of having bots act as 'Player' to create monsters, saves a shitton of coding and complexity in this project
      * second project would be config-driven bot Monsters, might need is_monster flag in this project though for some logic

  * Stats are as follows:   *(this will and must change)*
    * attack , int , starts at 1
    * defense , int , starts at 1
    * health , int , starts at 100

  * Stats could become:  *(check for trademark, although I might not care)*
    * All start at 1.
    * STR
      * increases melle attack and carry weight  *(is this a thing?)*

    * PER
      * increases ranged attack and reduces enemy def

    * END
      * increases health, damage
      * health = 20 + lvl\*2 + END\*2

lvl  | END | health  
-----|-----|------
1    |1    | 24      
2    |2    |  28     
5    |5    | 20      
2    |5    | 24      
10   |20   | 80      
20   |20   | 100     
50   |100  | 320     
100  |100  | 420  

---|---|---|---|---|---|---|---|---
lvl|1  |2  |2  |5  |10 |20 |50 |100
END|1 |2 |5 |5 |20 |20 |100 |100
health|24 |28 |34 |40 |80 |100 |320 |420

    * CHR
      * no fucking clue yet
      * increases gold? xp? 
      * not combat related? 

    * INT
      * no fucking clue yet
      * increase xp? lowers timer speeds?

    * AGI
      * slightly increases attack and increase defense

    * LCK
      * increases gold, crit

  * Fighting algorithm now:
    * min( 1, Ad6 - Dd6 ) , where A and D are attack and defense
    * so A of 5 and D of 6 would become  5d6 - 6d6  , or  (5 to 30)  minus (6 to 36)

  * Fighting algorithm could be:
    * min( 1, attack - defense )
    * attack =  (STR|PER)d6 + AGI + crit
      * nothing an enemy has reduces your attack

    * crit = min( 0 , (LCKd6)^2 - (LCKd6)^2)
      * 50% chance of zero, sliding chance of exponential

    * defense = enemy.ENDd6 + enemy.AGI - PERd6
      * your PER reduces enemy defense
      * this makes the game offense-heavy, but im ok with that

  * Equipment might be cool, but there are no plans to implement
    * Complicates everything. Might prefer this to be flavor-text only.
    * attack + "My massive enhanced rocket-powered flaming mini-nuke mjornir of burninateing does 1 damage..."
    * melee vs ranged? just a flag? keyword driven?
      * parse for keywords, tally, and decide? have result output in stats, so Players know

  * skills might be cool, but no plan to implement
    * same as equipment, only worse.
    * could be limited to effect + flavor-text
    * attack + "I cast lvl.99999999 Magic Missile for 1 damage...", now you have spells
    * heal as negative attack? temporary stat-boost skill? 

  * Death can occur, but isnt implemented
    * dead Players should'nt be able to attack, be victim, level up, etc..
      * make sure dying is un-fun, something to be avoided

    * need a way to revive, continue playing
      * rez one per hour/day/week ?
      * command-based cost? auto-deduct gold? loss of xp, levels, stats?

  * health exists, but there is no way to regenerate it
    * free potions? find potions? buy potions?
    * free health every hour/day/week?
      * command based on timer, or passive

    * combat healing skill? cost mana? gold? xp?  

  * health vs dying
    * dying is not just 0 health, you have to un-do the death
    * avoid dying; more than just "oh my health is low, lawl whatev"

  * admin command only does reload right now
    * should be able to manipulate any part of any Players anything
    * maybe even change say_hi and good_bye messages?
    * die command? 

  * monster commands
    * monster bots will need access to specialized admin-esque commands, to respawn and whatnot
    * implement a new command, `!monster` , check is_monster flag, hide from `!help` list


