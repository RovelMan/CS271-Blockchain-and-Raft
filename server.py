import sys, socket, threading, pickle, time, random
from block import printBlock, Block
from messages.raftMessage import Message
from messages.requestVote import RequestVote, RequestVoteResponse
from messages.appendEntry import AppendEntry
from states.candidate import *
from states.follower import *
import serverConfig
import clientConfig
import random

#serverState = {'follower': 0, 'candidate': 1, 'leader': 2}

class Server(object):

  def __init__(self, id, state):
    if ((id != 'x') and (id != 'y') and (id != 'z')):
		  print("Error! Invalid Server ID \nHas to be x, y or z \nQuitting...")
		  return

    self.blockchain = []
    self.tempTxns = []

    self.id = id
    self.host = "127.0.0.1"
    self.port = serverConfig.SERVER_PORTS[id]
    self.message = None
    self.currentState = state
    self.log = {}
    self.commitIndex = 0
    self.currentTerm = 0
    self.lastLogTerm = 0
    self.lastLogIndex = 0
    print("Setup for Server" + self.id.upper() + " done!")
    self.run()

  def run(self):
    self.initializeAllThreads()
    self.setupCommandTerminal()

  def initializeAllThreads(self):
    socketThread = threading.Thread(target=self.setupListeningSocket, args=(self.host, self.port))
    timeout = random.randint(6,20)
    timerThread = threading.Thread(target=self.setupTimer, args=(timeout,))
    socketThread.daemon, timerThread.daemon = True, True
    socketThread.start()
    timerThread.start()

  def setupCommandTerminal(self):
    command = ''
    while command != 'q':
      print("Commands:")
      print("\tSee blockchain: b")
      print("\tQuit: q")
      command = raw_input("Enter command: ")
      if command == 'q':
        print("Quitting")
        break
      elif command == 'b':
        print("Printing blockchain...")
        for block in self.blockchain:
          printBlock(block)
      else:
        print("Invalid command! Try again...")

  def setupListeningSocket(self, host, port):
    listeningPort = socket.socket()
    listeningPort.bind((host, port))
    listeningPort.listen(5)
    while True:
      conn, addr = listeningPort.accept()
      data = conn.recv(1024)
      #print("Before unpickling: " + str(data))
      data_object = pickle.loads(data)
      print("Message recieved: " + str(data_object))
      if (isinstance(data_object, RequestVoteResponse)):
        self.message = "STOP"
        if(isinstance(self.currentState, Candidate)):
            self.currentState.handleResponseVote(self, data_object)
        continue
      elif (isinstance(data_object, RequestVote)):
        self.message = "STOP"
        print("I got request vote")
        self.currentState.respondToRequestVote(self, data_object)
      elif (isinstance(data_object, AppendEntry)):
          if(data_object.entries == []):
            print("Got heartbeat")
      elif (isinstance(data_object, str)):
        trans = data_object
        print("Transaction received!", trans)
        self.tempTxns.append(trans)
        if len(self.tempTxns) == 2:
          self.addToBlockchain(self.tempTxns)
          self.sendMoneyUpdateToClients(self.tempTxns)
          self.tempTxns = []
      else:
        print("K bye")
      conn.close()

  def setupTimer(self, interval=1):
    currentInterval = interval
    while True:
      time.sleep(1)
      if currentInterval == 0:
        print("Message recieved!")
        self.currentState = Candidate()
        self.currentState.startElection(self)
        return
      if self.message == "STOP":
          print("Timer stopped")
          break
      else:
        print('Timer: ' + str(currentInterval) + ' seconds left')
        currentInterval -= 1

  def addToBlockchain(self, txns):
    block = Block(self.currentTerm, txns)
    block.hash_block()
    if len(self.blockchain) == 0:
      block.hash_prev_block(None)
    else:
      block.hash_prev_block(self.blockchain[len(self.blockchain)-1])
    self.blockchain.append(block)

  def sendMoneyUpdateToClients(self, txns):
    clientPorts = clientConfig.CLIENT_PORTS
    for clientId in clientPorts:
      for trans in txns:
        if trans.split(' ')[0].lower() == clientId or trans.split(' ')[1].lower() == clientId:
          try:
            s = socket.socket()
            s.connect((self.host, clientPorts[clientId]))
            s.send(pickle.dumps(trans))
            s.close()
          except:
            print("Client" + str(clientId).upper() + " is down!") 

if __name__ == '__main__':
  state = Follower()
  server = Server(sys.argv[1], state)
