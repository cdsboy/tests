import datetime
import random
import copy

CHANNEL = "##vapergames"

PLAYER_TYPE_SETS = {
    4: ['vampire', 'vampire', 'angel', 'townsfolk'],
    5: ['vampire', 'vampire', 'angel', 'townsfolk', 'townsfolk'],
    6: ['vampire', 'vampire', 'angel', 'seer', 'townsfolk', 'townsfolk'],
    7: ['vampire', 'vampire', 'angel', 'seer', 'townsfolk', 'townsfolk',
        'townsfolk'],
    8: ['vampire', 'vampire', 'vampire', 'angel', 'seer', 'townsfolk',
        'townsfolk', 'townsfolk'],
    9: ['vampire', 'vampire', 'vampire', 'angel', 'seer', 'townsfolk',
        'townsfolk', 'townsfolk', 'townsfolk'],
    10: ['vampire', 'vampire', 'vampire', 'angel', 'seer', 'seer', 'townsfolk',
         'townsfolk', 'townsfolk', 'townsfolk'],
}

PLAYER_ANNOUNCE = {
    4: "There are 2 vampires, an angel, and a townsfolk in this game.",
    5: "There are 2 vampires, an angel, and 2 townsfolk in this game.",
    6: "There are 2 vampires, an angel, a seer, and 2 townsfolk in this game.",
    7: "There are 2 vampies, an angel, a seer, and 3 townsfolk in this game.",
    8: "There are 3 vampires, an angel, a seer, and 3 townsfolk in this game.",
    9: "There are 3 vampires, an angel, a seer, and 4 townsfolk in this game.",
    10: "There are 3 vampires, an angel, 2 seers, and 4 townsfolk in this game."
}

class VampireBot(object):
  def __init__(self):
    self.startingPlayers = []
    self.killed = []
    self.players = {}
    self.owner = ''
    self.playing = False
    self.started = False
    self.isDay = True
    self.vampires = []
    self.seers = []
    self.victim = ''
    self.potentialVictim = ''
    self.blessed = ''
    self.dreams = {}
    self.votes = []

  def start(self, jenni, owner):
    self.owner = owner
    if self.playing or self.started:
      jenni.msg(CHANNEL, "%s: There is already a game of Vampires started." % owner)
    else:
      self.lastActive = datetime.datetime.now()
      self.playing = True
      jenni.msg(CHANNEL, "%s has started a new game of Vampires! Type .vjoin to join the game. Vampires requires a minimum of 4 players. %s can start the game by typing .vstart once all players have joined. The owner can stop the game at any time by typing .vstop" % (owner, owner))
      self.startingPlayers.append(owner)

  def stop(self, jenni, owner):
    if owner != self.owner:
      jenni.msg(CHANNEL, "You cannot stop this game because you are not the owner.")
    else:
      jenni.msg(CHANNEL, "This game of vampires is now over.")
      self.startingPlayers = []
      self.killed = []
      self.players = {}
      self.owner = ''
      self.playing = False
      self.started = False
      self.isDay = True
      self.vampires = []
      self.seers = []
      self.victim = ''
      self.potentialVictim = ''
      self.blessed = ''
      self.dreams = {}
      self.votes = []

  def join(self, jenni, player):
    if self.started:
      jenni.msg(CHANNEL, "%s: There is already a game of Vampires going on." % player)
    if self.playing:
      self.startingPlayers.append(player)
      jenni.msg(CHANNEL, "%s has joined the game. We currently have %s players."
                % (player, len(self.startingPlayers)))
    else:
      jenni.msg(CHANNEL, "%s: There is currently no game of Vampires started. Type .vampires to start" % player)

  def leave(self, jenni, player):
    if player == self.owner:
      jenni.msg(CHANNEL, "%s: You are the owner of this game and cannot leave. Please end the game if you want to quit playing." % player)
    else:
      if player in self.startingPlayers:
        self.startingPlayers.remove(player)
      if player in self.players:
        del self.players[player]
      if player in self.killed:
        self.killed.remove(player)

  def start_game(self, jenni, owner):
    startingNum = len(self.startingPlayers)
    if self.owner != owner:
      jenni.msg(CHANNEL, "%s: You are not the owner of this game!" % owner)
    if startingNum < 4:
      jenni.msg(CHANNEL, "There are not enough players to start a game of Vampires! You need atleast 4 players.")
    else:
      players = random.shuffle(self.startingPlayers)
      for i in xrange(startingNum):
        self.players[players[i]] = PLAYER_TYPE_SETS[startingNum][i]
        if PLAYER_TYPE_SETS[startingNum][i] == 'vampire':
          self.vampires.append(players[i])
        elif PLAYER_TYPE_SETS[startingNum][i] == 'seer':
          self.seers.append(players[i])

      for player, type in self.players.iteritems():
        if type == 'vampire':
          fellows = copy.deepcopy(self.vampires)
          fellows.remove(player)
          notice = 'You are a vampire! '
          if len(fellows) == 1:
            notice += "Your fellow vampire is %s. Please talk to your fellow and agree on someone to kill during the night. You both need to message me the command .vkill name of who you decide." % fellows[0]
          else:
            notice += "Your fellow vampires are %s. " % " and ".join(fellows)

          jenni.notice(player, notice) 
        if type == 'angel':
          jenni.notice(player, "You are an angel! During the night you message me the name of a person to bless and save from dying. You do this by typing .vbless name in a private message.")
        elif type == 'seer':
          jenni.notice(player, "You are a seer! During the night you message me the name of a person to dream about. This will tell you what they are up to in the night. You do this by typing .vdream name in a private message.")
        else:
          jenni.notice(player, "You are a townsfolk!")
      
      jenni.msg(CHANNEL, "The game has started! Your day was peaceful, but now night is upon us. Players who can act in the night please message me with your actions.")
      self.isDay = False
      self.started = True

  def kill(self, jenni, player, victim):
    if self.players[player] != 'vampire':
      jenni.notice(player, "You are not a vampire! You cannot kill anyone.")
    elif self.isDay:
      jenni.notice(player, "You cannot kill someone during the day!")
    else:
      if not victim in self.players or victim in self.killed or self.players[player] == 'vampire':
        jenni.notice(player, "That is not a valid player to kill!")
      elif not self.victim and not self.potentialVictim:
        self.potentialVictim = victim
      elif not self.victim and self.potentialVictim:
        if self.potentialVictim == victim:
          self.victim = victim
        else:
          for vampire in self.vampires:
            jenni.notice(vampire, "You and your fellow vampires have disagreed on who to kill! Please talk it over and resubmit your selection.")
          self.potentialVictim = ''
      elif self.victim:
        jenni.notice(player, "You already agreed on a victim!")
      self.check_night(jenni)

  def bless(self, jenni, player, blessed):
    if self.players[player] != 'angel':
      jenni.notice(player, "You are not an angel! You cannot save someone.")
    elif self.isDay:
      jenni.notice(player, "You cannot save someone during the day!")
    elif blessed not in self.players or blessed in self.killed:
      jenni.notice(player, "You cannot bless that person. Please bless someone else.")
    else:
      self.blessed = blessed
      self.check_night(jenni)

  def dream(self, jenni, player, selected):
    if self.players[player] != 'seer':
      jenni.notice(player, "You are not a seer! You cannot dream about someone.")
    elif self.isDay:
      jenni.notice(player, "You cannot dream during the day!")
    elif selected not in self.players or selected in self.killed:
      jenni.notice(player, "You cannot dream about that person. Please choose someone else.")
    else:
      self.dreams[player] = selected
      self.check_night(jenni)

  def check_night(self, jenni):
    if self.victim and len(self.dreams) == len(self.seers) and self.blessed:
      msg = "The sun has risen and the night has ended. "
      if self.victim == self.blessed:
        msg += "There were no victims last night! You all live to see another day. "
      else:
        msg += "Unfortunately %s is no longer with us. " % self.victim
        self.killed.append(self.victim)
      msg += "Please talk with your peers and decide who to stake. Once you know who you'd like to kill type .stake name to lock in your decision. Note: If there is a tie I will decide which person to kill!"

      jenni.msg(CHANNEL, msg)

      self.victim = ''
      self.dreams = {}
      self.blessed = ''
      self.isDay = True

      self.check_over(jenni)

  def stake(self, jenni, player, selected):
    if selected not in self.players or selected in self.killed:
      jenni.msg(CHANNEL, "%s: That is not a valid player.")
    else:
      self.votes.append(selected)
      self.check_day(jenni)

  def check_day(self, jenni):
    if len(self.votes) == (len(self.players) - len(self.killed)):
      votes = {}
      for vote in self.votes:
        if vote in votes:
          votes[vote] = 1
        else:
          votes[vote] += 1

      choices = []
      max = 0
      for vote, num in votes.iteritems():
        if num > max:
          choices = [vote,]
          max = max
        elif num == max:
          choices.append(vote)
      
      killed = None
      if len(choices) == 1:
        killed = choices[0]
      else:
        killed = random.choice(choices)

      jenni.msg(CHANNEL, "You all decided to take a stake to %s. They are no longer with us and once again night has fallen. Players who can act during the night please message me with your actions." % killed)
      
      self.killed.append(killed)
      self.votes = []
      self.isDay = False

      self.check_over(jenni)

  def check_over(self, jenni):
    vampiresDead = True
    for vampire in self.vampires:
      if vampire not in self.killed:
        vampiresDead = False
        break
    if vampiresDead:
      jenni.msg(CHANNEL, "The living have succeded in killing all of the vampires! Congratulations to the living!")
      self.stop(jenni, self.owner)

    livingDead = True
    for player, type in self.players.iteritems():
      if type != 'vampire' and player not in self.killed:
        livingDead = False
        break

    if livingDead:
      jenni.msg(CHANNEL, "The vampires have killed everyone in the town! Congratulations to the vampires!")
      self.stop(jenni, self.owner)

vambot = VampireBot()

def vampires(jenni, input):
  print "vampires"
  if input.sender != CHANNEL:
    jenni.reply("Please join %s to play vampires!" % CHANNEL)
  else:
    vambot.start(jenni, input.nick)
vampires.commands = ['vampires']
vampires.priority = 'low'

def stop(jenni, input):
  print "stop"
  vambot.stop(jenni, input.nick)
stop.commands = ['vstop']
stop.priority = 'low'

def join(jenni, input):
  print "join"
  vambot.join(jenni, input.nick)
join.commands = ['vjoin']
join.priority = 'low'

def leave(jenni, input):
  print "leave"
  vambot.leave(jenni, input.nick)
leave.commands = ['vleave']
leave.priority = 'low'

def start(jenni, input):
  print "start"
  vambot.start_game(jenni, input.nick)
start.commands = ['vstart']
start.priority = 'low'

def check_input(jenni, input):
  split = input.split()
  if len(split) != 2:
    jenni.notice(input.nick, "Invalid command")
    return None
  return split[1]

def kill(jenni, input):
  print "kill"
  info = check_input(jenni, input)
  if info:
    vambot.kill(jenni, input.nick, info)
kill.commands = ['vkill']
kill.priority = 'low'

def bless(jenni, input):
  print "bless"
  info = check_input(jenni, input)
  if info:
    vambot.bless(jenni, input.nick, info)
bless.commands = ['vbless']
bless.priority = 'low'

def dream(jenni, input):
  print "dream"
  info = check_input(jenni, input)
  if info:
    vambot.dream(jenni, input.nick, info)
dream.commands = ['vdream']
dream.priority = 'low'

def stake(jenni, input):
  print "stake"
  split = input.split()
  if len(split) != 2:
    jenni.msg(CHANNEL, "Invalid Command")
  else:
    vambot.stake(jenni, input.nick, split[1])
stake.commands = ['vstake']
stake.priority = 'low'
