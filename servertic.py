
from socket import socket,AF_INET,SOCK_STREAM,gethostname,error


from threading import Thread

from sys import exit

from time import sleep


from tictactoe import Tictactoe


class ServerTic:

	def __init__(self):	
		self.tic = Tictactoe()
		board=[[0,0,0],[0,0,0],[0,0,0]]
		self.players ={
					'player1':None,
					'player2':None
				}
		self.server = socket(AF_INET,SOCK_STREAM)
		self.host = gethostname()
		self.port = 5000
		self.turno = None

		self.server.bind((self.host,self.port))
		self.server.listen(3)
			
		print("SERVER LISTENING ON ",self.host,self.port)
		self.turno=None
	
	def clientHandler(self,s,addr):

		print("El cliente ",addr[0],":",addr[1]," se ha conectado\n")
		
		buff=s.recv(1024)
		message=str(buff)
		print(buff)

		if not self.players['player1']:
			self.players['player1']=s
			s.send(self.encodeMsg("[Server Msg]- Te has conectado al servidor"))
			s.send(self.encodeMsg("[Server Msg]- Se te ha assignado el valor de jugador X"))
		else:
			self.players['player2']=s
			s.send(self.encodeMsg("[Server Msg]- Te has conectado al servidor"))
			s.send(self.encodeMsg("[Server Msg]- Se te ha assignado el valor de jugador O"))
			self.players['player1'].send(self.encodeMsg("[Server Msg]- Empezando el juego"))
			self.players['player2'].send(self.encodeMsg("[Server Msg]- Empezando el juego"))
		
		if not self.turno:
			self.turno="p1"

	def encodeMsg(slef,msg):

		return bytes(msg,'utf-8')


	
	def start(self):
		try:
			while True:

				if self.players['player1'] and not self.players['player2']:
					self.players['player1'].send("[Server Msg] Esperando jugador 2".encode("utf-8"))
					
				if self.players['player1'] and self.players['player2']:
					
					if self.turno == 'p1':
						
						self.players['player1'].send(self.encodeMsg("[Player Turn]"))
						self.players['player2'].send(self.encodeMsg("[Server Msg] Waiting for the openents movement...."))
						buff=self.players['player1'].recv(1024)
						self.tic.theBoard[buff.decode('ascii')]='X'
						if self.tic.comprobar('X'):
							self.players['player1'].send(self.encodeMsg("[Server Msg] Has ganado Felicidades"))
							self.players['player2'].send(self.encodeMsg("[Server Msg] Perdiste Caramono jajaj gil "))
							self.players['player1'].close()
							self.players['player2'].close()
						else:
							self.players['player2'].send(b"[Player Movement]"+buff)
							print("jugada del player 1",buff)
							self.turno='p2'
					else:
						
						self.players['player2'].send(self.encodeMsg("[Player Turn]"))
						self.players['player1'].send(self.encodeMsg("[Server Msg] Waiting for the openents movement...."))
						buff=self.players['player2'].recv(1024)
						self.tic.theBoard[buff.decode('ascii')]='O'

						if self.tic.comprobar('O'):
							self.players['player2'].send(self.encodeMsg("[Server Msg] Has ganado Felicidades"))
							self.players['player1'].send(self.encodeMsg("[Server Msg] Perdiste Caramono jajaj gil "))
							self.players['player1'].close()
							self.players['player2'].close()
						else:
							self.players['player1'].send(b"[Player Movement]"+buff)
							print("jugada del player 2",buff)
							self.turno='p1'

				else:
					
					s,addr=self.server.accept()
					self.clientHandler(s,addr)

					
		except error as e:
			print(e)
			exit()
			raise e






server = ServerTic()


server.start()