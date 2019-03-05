import sys, socket, threading, pickle, time, random

serverPorts = {'x': 7100, 'y': 7200, 'z': 7300}
serverState = {'follower': 0, 'candidate': 1, 'leader': 2}

class Server(object):

  def __init__(self, id):
    if ((id != 'x') and (id != 'y') and (id != 'z')):
		  print("Error! Invalid Server ID \nHas to be x, y or z \nQuitting...")
		  return
    self.id = id
    self.host = "127.0.0.1"
    self.port = serverPorts[id]
    self.message = None
    self.currentState = serverState['follower']
    print("Setup for Server" + self.id.upper() + " done!")
    socketThread = threading.Thread(target=self.setupListeningSocket, args=(self.host, self.port))
    timerThread = threading.Thread(target=self.setupTimer, args=(10,))
    socketThread.daemon, timerThread.daemon = True, True
    socketThread.start()
    timerThread.start()
    quitTerminal = ''
    while quitTerminal != 'q': 
      quitTerminal = raw_input("Write q to quit: ")
      if quitTerminal != 'q':
        print("Wrong input. Try Again!")
      else:
        print("Quitting")

  def setupListeningSocket(self, host, port):
    listeningPort = socket.socket()
    listeningPort.bind((host, port))
    listeningPort.listen(5)
    while True:
      conn, addr = listeningPort.accept()
      data = conn.recv(1024).decode()
      print("Message recieved: " + data)
      if (data == "STOP"):
        self.message = "STOP"
        break
      conn.close()

  def setupTimer(self, interval=1):
    currentInterval = interval
    while True:
      time.sleep(1)
      if self.message == "STOP":
        print("Message recieved! Timer stopped")
        return
      if currentInterval == 0 and self.message == None:
        self.startElection()
        # self.currentState = Candidate()
        # self.currentState.startElection()
        return
      else:
        print('Timer: ' + str(currentInterval) + ' seconds left')
        currentInterval -= 1

  def startElection(self):
    dkeys = serverPorts.keys()
    for d in dkeys:
      if (d != self.id):
        try:
          s = socket.socket()
          print("Sending STOP message to " + str(serverPorts[d]))
          s.connect(("127.0.0.1", serverPorts[d]))
          s.send("STOP")
          s.close()
        except:
          print("Server" + d.upper() + " is down!")
          continue
    print("Election Over")
  

if __name__ == '__main__':
  server = Server(sys.argv[1])
