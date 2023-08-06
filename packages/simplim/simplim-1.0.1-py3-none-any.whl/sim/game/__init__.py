import sim
import struct

class Player():
	def __init__(self, dict_ = {}, HP = 100, NP = 0, MP = 0, SP = 0, NDEF = 0, MDEF = 0, SDEF = 0, NATK = 0, MATK = 0, SATK = 0, LUCK = 50):
		if dict_:
			try:
				self.HP = dict_['HP']

				self.NP = dict_['NP']
				self.MP = dict_['MP']
				self.SP = dict_['SP']

				self.NDEF = dict_['NDEF']
				self.MDEF = dict_['MDEF']
				self.SDEF = dict_['SDEF']

				self.NATK = dict_['NATK']
				self.MATK = dict_['MATK']
				self.SATK = dict_['SATK']

				self.LUCK = dict_['LUCK']
			except:
				pass
		else:
			self.HP = HP

			self.NP = NP
			self.MP = MP
			self.SP = SP

			self.NDEF = NDEF
			self.MDEF = MDEF
			self.SDEF = SDEF

			self.NATK = NATK
			self.MATK = MATK
			self.SATK = SATK

			self.LUCK = LUCK
		

class TeamGame():
	def __init__(self, playerNum, type):
		self.players = set(())
		self.playersInfo = dict()

	def playerReady(self, player):
		self.players.add(player)

	def playerCancel(self, player):
		self.player.remove(player)

	def getPlayerInfo(self):
		for player in self.players:
			self.playersInfo[player] = 

	def start():
		pass


class Map():
	def __init__(self, map_, objList):
		self.map = map_
		for x in :
			pass
		

def makeMap():
	array=[[0x50,0x4b,0x3,0x4],
		[0x4,0x3a,0x92,0x83],
		[0x50,0x43,0x9b,0x16]]
	with open("testfile","wb") as fp:
	    for row in array:
	    	for block in row:
	        	s = struct.pack('B',block)
	        	fp.write(s)
	fp.close()









