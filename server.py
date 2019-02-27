import sys, socket, threading, pickle, time, random

serverPorts = {'x': 7100, 'y': 7200, 'z': 7300}


class Server(object):

  def __init__(self, id):
    self.id = id

  def startElection(self):
    dkeys = serverPorts.keys()
    for d in dkeys:
      if (d != self.id):
        s = socket.socket()
        print("Sending stop message to " + str(serverPorts[d]))
        s.connect(("127.0.0.1", serverPorts[d]))
        s.send("stop")
        s.close()
    print("election over")

class ListeningSocket(object):
  def __init__(self, id):
    if ((id != 'x') and (id != 'y') and (id != 'z')):
		  print("Error! Invalid Server ID \nHas to be x, y or z \nQuitting...")
		  return
    self.id = id
    self.host = "127.0.0.1"
    self.port = serverPorts[id]
    self.message = False
    self.listeningPort = socket.socket()
    self.listeningPort.bind((self.host, self.port))
    self.listeningPort.listen(5)
    print("Setup for Server" + self.id.upper() + " done!")
    self.run()

  def run(self):
    connections = HandleIncomingMessages(self.listeningPort)
    print("Running")
    wait = raw_input("What next: ")
    print(wait)

class HandleIncomingMessages(object):
  def __init__(self, listeningChannel):
    thread = threading.Thread(target=self.run(listeningChannel), args=())
    thread.daemon = True
    thread.start()

  def run(self, listeningChannel):
    print("ready")
    while True:
      t = Timeout(10)
      conn, addr = listeningChannel.accept()
      data = conn.recv(1024).decode()
      print("Message recieved:", data)
      if (data=="stop"):
          t.setMessage(data)
          break
      conn.close()

class Timeout(object):
  def __init__(self, interval=1):
    self.interval = interval
    self.message = None
    thread = threading.Thread(target=self.run, args=())
    thread.daemon = True
    thread.start()

  def setMessage(self, message):
    self.message = message

  def run(self):
    currentInterval = self.interval
    while True:
      time.sleep(1)
      if self.message == "stop":
        print("Message recieved! Timer stopped")
        return
      if currentInterval == 0:
        s = Server(sys.argv[1])
        s.startElection()
        # print('Timer resetting')
        # currentInterval = self.interval
        return
      else:
        print('Timer: ' + str(currentInterval) + ' seconds left')
        currentInterval -= 1

if __name__ == '__main__':
  server = ListeningSocket(sys.argv[1])
