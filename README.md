# irc_bot_test001
gonna experiment with making a game-focused irc bot


## Design Doc:

### Description:

This is an irc based idle-quest minigame bot. 

#### Design Goals:

Simple is better than complex. Complex is better than complicated.

I'd rather have a simple front end and a complex back end, than a simple backend and a complicated fromt end. 

The fewer unique commands the better. The fewer nested commands the more-better; OR better yet, not at all.  

#### Function Requirements: *(kinda)*


 * Players will be inducted into the database upon joining the channel.
 * Players may attack other players in the channel
   * Monsters will be separate bots, not in this code base
 * Players earn ?gold? for winning fights
   * Spend gold on what?
 * Players may increase their stats 
   * I want it to be timer-based, where the first stat is very quick, and additional stat increases take longer and longer. 
   * may also be XP based, must spend XP to initiate the timer
 * attacks, defends, and other actions may be madlib'able by each player
   * eg. : 
     * `!q setname bloodninja`
     * `!q setattack casts lvl.9999999 lightning bolt`
     * `!q setdefend I put on my hat and wizard robe`
   * this opens up the option of having bots act as 'Player' to create monsters, saves a shitton of coding and complexity in this project
     * second project would be config-driven bot Monsters, might need is_monster flag in this project though for some logic
 * Stats are as follows:  *(this will and must change)*
   * attack , int , starts at 1
   * defense , int , starts at 1
   * health , int , starts at 100

 * Stats could become: *(check for trademark, although I might not care)*
   * All start at 1.
   * STR
     * increases melle attack and carry weight *(is this a thing?)*
   * PER
     * increases ranged attack and reduces enemy def
   * END
     * increases health, damage
     * health = 20 + lvl*2 + END*2
        lvl  | END | health  
       ------------ | -------|------
        1    |1    | 24      
        2    |2    |  28     
        5    |5    | 20      
        2    |5    | 24      
        10   |20   | 80      
        20   |20   | 100     
        50   |100  | 320     
        100  |100  | 420     
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
   * Ad6 - Dd6 , where A dn D are attack and defense
   * so A of 5 and D of 6 would become  5d6 - 6d6  , or  (5 to 30)  minus (6 to 36)
 * Fighting algorithm could be:
   * min( 1, attack - defense )
   * attack =  (STR|PER)d6 + AGI + crit
     * nothing an enemy has reduces your attack
   * crit = min( 0 , LCKd6^2 - LCKd6^2)
     * 50% chance of zero, sliding chance of exponential
   * defense = enemy.ENDd6 + enemy.AGI - PERd6
     * your PER reduces enemy defense


