import sys, socket, pickle, threading, time, clientConfig
from messages.serverToClient import ServerToClient

class Client(object):

  def __init__(self, id):
    if ((id != 'a') and (id != 'b') and (id != 'c')):
      print("Error! Invalid Client ID \nHas to be a, b or c \nQuitting...")
      return
    self.id = id
    self.host = "127.0.0.1"
    self.port = clientConfig.CLIENT_PORTS[id]
    self.serverPort = 7100
    self.amount = 1000
    with open("clientInputFile.txt", "r") as f:
      transactions = f.readlines()
    self.transactions = [x.strip() for x in transactions]
    print("Setup for Client" + id.upper() + " done!")
    self.run()

  def run(self):
    self.initializeAllThreads()
    self.setupCommandTerminal()

  def initializeAllThreads(self):
    socketThread = threading.Thread(target=self.setupListeningSocket, args=(self.host, self.port))
    timerThread = threading.Thread(target=self.setupTimer)
    socketThread.daemon, timerThread.daemon = True, True
    socketThread.start()
    timerThread.start()

  def setupCommandTerminal(self):
    command = ''
    while command != 'q':
      print("Commands:")
      print("\tMake transaction: m")
      print("\tQuit: q")
      command = raw_input("Enter command: ")
      if command == 'q':
        print("Quitting")
      elif command == 'm':
        self.makeTransaction()
      else:
        print("Invalid command! Try again...")

  def setupListeningSocket(self, host, port):
    listeningPort = socket.socket()
    listeningPort.bind((host, port))
    listeningPort.listen(5)
    while True:
      conn, addr = listeningPort.accept()
      data = conn.recv(1024)
      data_object = pickle.loads(data)
      print("Message recieved: " + str(data_object))
      if (isinstance(data_object, str)):
        # Add if statement for ack-string from server when transaction is comitted
        trans = data_object
        print("Transaction received!", trans)
        self.recieveMoneyFromClient(trans)
      elif (isinstance(data_object, ServerToClient)):
        print("Now the leader is: " + str(data_object.leaderPort))
        self.serverPort = data_object.leaderPort
      else:
        print("K bye")
      conn.close()

  def setupTimer(self, interval=1):
    time.sleep(10)
    while True:
      for trans in self.transactions:
        if trans.split(" ")[0] == self.id.upper():
          self.sendMoneyToClient(trans)
        time.sleep(1)
      print("No more transactions")
      break

  def sendMoneyToClient(self, trans):
    self.amount -= int(trans.split(' ')[2])
    try:
      s = socket.socket()
      print("Sending amount " + str(trans[2]) + " to " + str(trans[1]))
      s.connect((self.host, self.port))
      s.send(pickle.dumps(trans))
      s.close()
    except:
      print("Client " + str(trans[2]) + " is down!")

  def recieveMoneyFromClient(self, trans):
    self.amount += int(trans.split(' ')[2])
    self.tellServer(trans)

  def tellServer(self, trans):
    try:
      s = socket.socket()
      print("Sending transaction to server " + str(self.serverPort))
      s.connect((self.host, self.serverPort))
      s.send(pickle.dumps(trans))
      s.close()
    except:
      print("Server " + str(self.serverPort) + " is down!")
    return

  def makeTransaction(self):
    reciever = raw_input("To whom? (b or c) ")
    amount = raw_input("How much? ")
    try:
      s = socket.socket()
      print("Sending transaction to " + str(self.serverPort))
      s.connect(("127.0.0.1", self.serverPort))
      s.send(pickle.dumps(str(self.id).upper() + " " + str(reciever).upper() + " " + str(amount)))
      s.close()
    except:
      print("Server" + 'x'.upper() + " is down!")

if __name__ == '__main__':
  client = Client(sys.argv[1])

  command = ''
  while command != 'q':
    print("Commands:")
    print("\tMake transaction: m")
    print("\tQuit: q")
    command = raw_input("Enter command: ")
    if command == 'q':
      print("Quitting")
    elif command == 'm':
      reciever = raw_input("To whom? (b or c) ")
      amount = raw_input("How much? ")
      try:
        s = socket.socket()
        print("Sending transaction to " + str(7100))
        s.connect(("127.0.0.1", 7100))
        s.send(pickle.dumps("A " + str(reciever).upper() + " " + str(amount)))
        s.close()
      except:
        print("Server" + 'x'.upper() + " is down!")
    else:
      print("Invalid command! Try again...")
