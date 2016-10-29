from serial import *
import json
from time import sleep


class LittleFreeLibrary(object):
	"""docstring for ClassName"""
	def __init__(self, serialPort):
		super(LittleFreeLibrary, self).__init__()
		self.serialPort = serialPort
		self.lastCommandError = 0 	
		self.programs = {	'no programs - must reload': '0'}
		self.customLED = [{'ledNumber':0, 'r':0, 'g':0, 'b':0}, 
						  {'ledNumber':1, 'r':0, 'g':0, 'b':0},
						  {'ledNumber':2, 'r':0, 'g':0, 'b':0},
						  {'ledNumber':3, 'r':0, 'g':0, 'b':0},
						  {'ledNumber':4, 'r':0, 'g':0, 'b':0},
						  {'ledNumber':5, 'r':0, 'g':0, 'b':0}
		]
		self.prefix = '||'
		self.getProgramsCommand()
		if len(self.programs) < 2:
			print("second try to lenoad commands")
			self.getProgramsCommand() #try a second time?


		# if the command hasn't every been run, negative -1, if has been run and a problem will do 0, if been run and ok 1


		# for key, value in j:
		# 	setattr(self,key,value)

	def sendCommand(self, command):

		response = " "
		#openBrace = 0
		#closeBrace = -1

		self.serialPort.flushInput() #empty 
		self.serialPort.write(bytes(command)) #send command
		sleep(4)
		response = self.serialPort.read(2000) #read up to 400

		# need to restructure this so it 1) loads all serial into buffer. 
		#Tries to json parse buffer. if fail then just still allow for commands


		#while self.charBalanced(response) < 1:
			# linefeed = '\n\r'

		#	byte = self.serialPort.read()
			# if byte not in linefeed:
		#	response += byte

			# print(response)
			# j = json.loads(response)
		# print response
		#response = response[len(command)+1:] 
		# always update the current program and command status to stay in sync.
		try:
			j = json.loads(response)

			self.currentProgram = j['currentProgram']

			if 'ledNumber' in j: 
				for led in self.customLED:
					if led['ledNumber'] == j['ledNumber']:
						led['r'] = j['r'] # assign LED to proper value.
						led['g'] = j['g'] # assign LED to proper value.
						led['b'] = j['b'] # assign LED to proper value.

			if 'programs' in j:
				self.programs = j['programs']
				self.customLED = j['customLED']
				self.prefix = j['commandPrefix']
				print("parsed a program!")

			self.lastCommandError = 0
			#print(" The Parsed Response :(  >>>> \n {} \n<<<<  ".format(response))

		except ValueError:
			#print(" The Unparsable Response :(  >>>> \n {} \n<<<<  ".format(response))
			print("no JSON parseable")
			print("\n------response------\n")
			print(response)
			print("\n----response end-----\n")
			self.lastCommandError = 1
		return response
		
	@staticmethod
	def charBalanced(theString):
		"""Parses string to see if it is balanced"""
		closers = {'{':'}','(':')','[':']'}
		stack = []
		balancedChar = 0


		for i, char in enumerate(theString):
			print('thestack: {}'.format(stack) )
			if char in closers.keys():
				stack.append(char)
				balancedChar = -1 
				print("adding to stack: {}".format(char))
			elif char in closers.values():
				if len(stack) > 0:
					lastChar = stack.pop()
				else: 
					return -1
				print('char is {} and  is {} and '.format(char, lastChar))
				if char == closers[lastChar]:
					stack.append(char)
					balancedChar = i
					print("not added to stack: {}".format(char))
				else:
					return -1 #not balanced because the last stack
		 	else:
		 		print("non important char: {}".format(char))
		print('now the stack {}'.format(stack))
		if len(stack) == 0:
			return balancedChar
		else:
			return -1

	def __str__(self):
		out = ''

		for program in self.programs:
			p = program['programName']
			c = self.prefix + program['programCode']
			out = out + ("Program '{}' can be called with code '{}'\n\r".format(p, c))
		return out	

	def getProgramsCommand(self):
		return self.sendCommand('|||||||0')


if __name__ ==  '__main__':
   
	Response = sendCommand('||||||||0')
	# print('this is the Response:\n')
	# print(Response)

	# print('this is the Response:\n')
	j = json.loads(Response)
	printProgramsFromJSON(j)