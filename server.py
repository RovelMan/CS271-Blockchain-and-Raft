import sys, socket, threading, pickle, time, random
from messages.raftmessage import  Message
from messages.requestVote import RequestVote, RequestVoteResponse
from messages.appendEntry import AppendEntry
from states.candidate import *
from states.follower import *
import serverConfig

serverState = {'follower': 0, 'candidate': 1, 'leader': 2}

class Server(object):

  def __init__(self, id, state):
    if ((id != 'x') and (id != 'y') and (id != 'z')):
		  print("Error! Invalid Server ID \nHas to be x, y or z \nQuitting...")
		  return
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
    self.initializeAllThreads()
    self.setupQuitting()

  def setupQuitting(self):
    quitTerminal = ''
    while quitTerminal != 'q':
      quitTerminal = raw_input("Write q to quit: ")
      if quitTerminal != 'q':
        print("Wrong input. Try Again!")
      else:
        print("Quitting")


  def initializeAllThreads(self):
    socketThread = threading.Thread(target=self.setupListeningSocket, args=(self.host, self.port))
    timerThread = threading.Thread(target=self.setupTimer, args=(10,))
    socketThread.daemon, timerThread.daemon = True, True
    socketThread.start()
    timerThread.start()


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
        self.currentState.handleResponseVote(self, data_object)
        continue
      elif (isinstance(data_object, RequestVote)):
        self.message = "STOP"
        print("I got request vote")
        self.currentState.respondToRequestVote(self, data_object)
      elif (isinstance(data_object, AppendEntry)):
          print("Got heartbeat")
      else:
        print("K bye")
      conn.close()

  def setupTimer(self, interval=1):
    currentInterval = interval
    while True:
      time.sleep(1)
      # if self.message == "STOP":
      #   print("Message recieved! Timer stopped")
      #   return
      if currentInterval == 0:
        print("Message recieved!")
        self.currentState = Candidate()
        self.currentState.startElection(self)
        # self.currentState = Candidate()
        # self.currentState.startElection()
        return
      if self.message == "STOP":
          print("Timer stopped")
          break
      else:
        print('Timer: ' + str(currentInterval) + ' seconds left')
        currentInterval -= 1

if __name__ == '__main__':
  state = Follower()
  server = Server(sys.argv[1], state)
