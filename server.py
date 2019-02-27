import sys
import socket
import threading

class Server(object):

  def __init__(self, id):
    if ((id != 'x') and (id != 'y') and (id != 'z')):
		  print("Error! Invalid Server ID \nHas to be x, y or z \nQuitting...")
		  return
    self._id = id
    self._serverPorts = {'x': 7100, 'y': 7200, 'z': 7300}
    self._host = "127.0.0.1"
    self._port = self._serverPorts[id]
    self._listeningPort = socket.socket()
    self._listeningPort.bind((self._host, self._port))
    self._listeningPort.listen(5)
    print("Setup for Server" + id.upper() + " done!")
    self.run()

  def run(self):
    connections = self.HandleIncomingMessages(self._listeningPort)

  class HandleIncomingMessages(object):

    def __init__(self, listeningChannel):
      thread = threading.Thread(target=self.run(listeningChannel), args=())
      thread.daemon = True
      thread.start()

    def run(self, listeningChannel):
      print("ready")
      while True:
        conn, addr = listeningChannel.accept()
        data = conn.recv(1024).decode()
        print("Message recieved:", data)
        conn.close()

if __name__ == '__main__':
  server = Server(sys.argv[1])
