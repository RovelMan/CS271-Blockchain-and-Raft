import sys, socket, threading, pickle, time, random
from block import printBlock, Block
from messages.raftMessage import Message
from messages.requestVote import RequestVote, RequestVoteResponse
from messages.appendEntry import AppendEntry, AcceptAppendEntry
from states.candidate import *
from states.follower import *
# from states.leader import *
import serverConfig
import clientConfig
import random

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

    self.currentInterval = 0
    self.interval = random.randint(12,15)
    self.defaultInterval = 8

    print("Setup for Server" + self.id.upper() + " done!")
    self.run()

  def run(self):
    self.initializeAllThreads()
    self.setupCommandTerminal()

  def initializeAllThreads(self):
    socketThread = threading.Thread(target=self.setupListeningSocket, args=(self.host, self.port))
    timeout = random.randint(6,20)
    timerThread = threading.Thread(target=self.setupTimer, args=(timeout,))
    # timerThread = threading.Thread(target=self.setupTimer, args=(self.interval,))
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
        print("Length of blockchain: " + str(len(self.blockchain)))
      else:
        print("Invalid command! Try again...")

  def setupListeningSocket(self, host, port):
    listeningPort = socket.socket()
    listeningPort.bind((host, port))
    listeningPort.listen(5)
    while True:
      conn, addr = listeningPort.accept()
      data = conn.recv(51200)
      #print("Before unpickling: " + str(data))
      data_object = pickle.loads(data)
      #print("Message recieved: " + str(data_object))
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
          self.currentState.answerLeader(self, data_object)
            # for x in range(len(self.blockchain)):
            #   print(self.blockchain[x])
            # self.currentInterval = self.defaultInterval
      elif (isinstance(data_object, AcceptAppendEntry)):
        if not data_object.acceptEntry:
          # TODO: Send the whole blockchain to the asker
          self.currentState.sendWholeBlockchain(self, data_object)
          
      elif (isinstance(data_object, str)):
        trans = data_object
        print("Transaction received!", trans)
        self.tempTxns.append(trans)
        if (len(self.tempTxns) == 2 and isinstance(self.currentState,Leader)):
          self.addToBlockchain(self.tempTxns)
          self.sendMoneyUpdateToClients(self.tempTxns)
          self.tempTxns = []
      elif (isinstance(data_object, list)):
        print("Got whole BLOCKCHAIN")
        self.blockchain = data_object
        self.lastLogIndex = len(data_object)
      else:
        print("K bye")
      conn.close()

  def setupTimer(self, interval=1):
    self.currentInterval = self.interval
    print('Timer: ' + str(self.currentInterval) + ' seconds left')
    while True:
      time.sleep(1)
      if self.currentInterval == 0:
        #print("Message recieved!")
        if(isinstance(self.currentState,Leader)):
          self.currentState.sendHeartbeatToAll(self)
          self.currentInterval = self.defaultInterval
          # print('Timer: ' + str(self.currentInterval) + ' seconds left')
          continue
        print("Timed out!")
        self.currentState = Candidate()
        self.currentState.startElection(self)
        while(isinstance(self.currentState, Candidate)):
            time.sleep(1)
        continue
      # if self.currentInterval == 5 and isinstance(self.currentState, Leader):
      #   self.currentState.sendHeartbeat(self)
      if self.message == "STOP":
          self.message = None
          if ( not (isinstance(self.currentState, Leader))):
              self.currentInterval = self.interval
              # print('Timer: ' + str(self.currentInterval) + ' seconds left')
          print("Timer reset")
          continue
      else:
        # print('Timer: ' + str(self.currentInterval) + ' seconds left')
        self.currentInterval -= 1

  def addToBlockchain(self, txns):
    block = Block(self.currentTerm, txns)
    block.hash_block()
    if len(self.blockchain) == 0:
      block.hash_prev_block(None)
    else:
      block.hash_prev_block(self.blockchain[len(self.blockchain)-1])
    self.lastLogIndex = len(self.blockchain) + 1
    self.blockchain.append(block)
    if(isinstance(self.currentState, Leader)):
        print("I am going to now append the block")
        self.currentState.startAppendEntry(self, block)

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
