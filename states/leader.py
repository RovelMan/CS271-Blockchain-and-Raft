from server import *
from messages.appendEntry import AppendEntry
import socket
import serverConfig

class Leader:

    def __init__(self):
        self.nextIndex = 0

    def initiateLeader(self, server):
        self.nextIndex = server.lastLogIndex + 1
        sender = server.id
        for recID in serverConfig.SERVER_PORTS.keys():
            if (recID != sender):
                heartbeat = AppendEntry(
                    server.currentTerm, server.id, serverConfig.SERVER_PORTS[recID], server.id, server.lastLogTerm, server.lastLogIndex, [], 0
                )
                self.sendHeartbeat(heartbeat)
        print("Heartbeat sent")

    def sendHeartbeat(self, heartbeat):
        try:
            s = socket.socket()
            print("Sending HEARTBEAT to " + str(heartbeat.receiver))
            s.connect(("127.0.0.1", heartbeat.receiver))
            dataString = pickle.dumps(heartbeat)
            s.send(dataString)
            s.close()
        except socket.error as e:
            for id, port in serverConfig.SERVER_PORTS.items():
                if port == heartbeat.receiver:
                    print(str(id).upper()+" is down")
