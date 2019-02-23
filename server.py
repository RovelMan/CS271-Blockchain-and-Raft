import sys
import socket

host, listeningPort, myId = None, None, None
myPort = 0
serverPorts = {'x': 7100, 'y': 7200, 'z': 7300}

def init(id):
  global host, listeningPort, myId, myPort
  if ((id != 'x') and (id != 'y') and (id != 'z')):
		print("Error! Invalid server ID \nHas to be x, y or z \nQuitting...")
		return
  myId = id
  host = "127.0.0.1"
  myPort = serverPorts[id]
  listeningPort = socket.socket()
  listeningPort.bind((host, myPort))
  listeningPort.listen(5)
  print("Setup for server " + id + " done!")

if __name__ == '__main__':
  init(sys.argv[1])
  print(host, listeningPort, myId, myPort)
