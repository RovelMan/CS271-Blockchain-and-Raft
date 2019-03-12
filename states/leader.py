from server import *
from messages.appendEntry import AppendEntry
from messages.serverToClient import ServerToClient
import socket
import serverConfig
import clientConfig

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
                print("Sending HEARTBEAT to " + str(heartbeat.receiver))
                self.informLeaderStatus(heartbeat)
        print("Heartbeat sent")
        for clientID in clientConfig.CLIENT_PORTS.keys():
            message = ServerToClient(
                server.currentTerm, server.id, clientConfig.CLIENT_PORTS[clientID], serverConfig.SERVER_PORTS[server.id]
            )
            self.informLeaderStatus(message)
        print("Clients informed")

    def informLeaderStatus(self, heartbeat):
        try:
            s = socket.socket()
            print("Sending initial HEARTBEAT to " + str(heartbeat.receiver))
            s.connect(("127.0.0.1", heartbeat.receiver))
            dataString = pickle.dumps(heartbeat)
            s.send(dataString)
            s.close()
        except socket.error as e:
            if(heartbeat.receiver/7000 < 1):
                for id2, port2 in clientConfig.CLIENT_PORTS.items():
                    if port2 == heartbeat.receiver:
                        print(str(id2).upper()+" is down")
            else:
                for id, port in serverConfig.SERVER_PORTS.items():
                    if port == heartbeat.receiver:
                        print(str(id).upper()+" is down")

    def startAppendEntry(self, server, block):
        sender = server.id
        for recID in serverConfig.SERVER_PORTS.keys():
            if (recID != sender):
                apmessage = AppendEntry(
                    server.currentTerm, server.id, serverConfig.SERVER_PORTS[recID], server.id,
                    server.lastLogTerm, server.lastLogIndex, [block], 0
                )
                print("Sending APPENDENTRY to " + str(apmessage.receiver))
                self.sendHeartbeat(apmessage)
        print("Sent AppendEntries to all servers")
        
    def sendHeartbeat(self, heartbeat):
        try:
            s = socket.socket()
            s.connect(("127.0.0.1", heartbeat.receiver))
            dataString = pickle.dumps(heartbeat)
            s.send(dataString)
            s.close()
        except socket.error as e:
            if(heartbeat.receiver/7000 < 1):
                for id2, port2 in clientConfig.CLIENT_PORTS.items():
                    if port2 == heartbeat.receiver:
                        print(str(id2).upper()+" is down")
            else:
                for id, port in serverConfig.SERVER_PORTS.items():
                    if port == heartbeat.receiver:
                        print(str(id).upper()+" is down")

