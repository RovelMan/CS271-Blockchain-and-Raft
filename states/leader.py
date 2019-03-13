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
        self.sendHeartbeatToAll(server)
        print("First Heartbeat sent")
        for clientID in clientConfig.CLIENT_PORTS.keys():
            message = ServerToClient(
                server.currentTerm, server.id, clientConfig.CLIENT_PORTS[clientID], serverConfig.SERVER_PORTS[server.id]
            )
            self.sendMessageToSocket(message)
        print("Clients informed")
        server.currentInterval = server.defaultInterval
        print("Reset my timer to defaultInterval")

    def sendHeartbeatToAll(self, server):
        for recID in serverConfig.SERVER_PORTS.keys():
            if (recID != server.id):
                heartbeat = AppendEntry(
                    server.currentTerm, server.id, serverConfig.SERVER_PORTS[recID], server.id, server.lastLogTerm, server.lastLogIndex, [], 0
                )
                #print("Sending INITIAL HEARTBEAT ANNOUNCEMENT to " + str(heartbeat.receiver))
                self.sendMessageToSocket(heartbeat)

    def sendMessageToSocket(self, appendEntryMessage):
        try:
            s = socket.socket()
            #print("Sending initial HEARTBEAT to " + str(heartbeat.receiver))
            s.connect(("127.0.0.1", appendEntryMessage.receiver))
            dataString = pickle.dumps(appendEntryMessage)
            s.send(dataString)
            s.close()
        except socket.error as e:
            if(appendEntryMessage.receiver/7000 < 1):
                for id2, port2 in clientConfig.CLIENT_PORTS.items():
                    if port2 == appendEntryMessage.receiver:
                        print(str(id2).upper()+" is down")
            else:
                for id, port in serverConfig.SERVER_PORTS.items():
                    if port == appendEntryMessage.receiver:
                        print(str(id).upper()+" is down")

    def startAppendEntry(self, server, block):
        sender = server.id
        for recID in serverConfig.SERVER_PORTS.keys():
            if (recID != sender):
                apmessage = AppendEntry(
                    server.currentTerm, server.id, serverConfig.SERVER_PORTS[recID], server.id,
                    server.lastLogTerm, server.lastLogIndex-1, [block], 0
                )
                print("Sending APPENDENTRY to " + str(apmessage.receiver))
                self.sendMessageToSocket(apmessage)
        print("Sent AppendEntries to all servers")

    def sendWholeBlockchain(self, server, data):
        try:
            s = socket.socket()
            s.connect(("127.0.0.1", serverConfig.SERVER_PORTS[data.sender]))
            dataString = pickle.dumps(server.blockchain)
            s.send(dataString)
            s.close()
        except socket.error as e:
            if(appendEntryMessage.receiver/7000 < 1):
                for id2, port2 in clientConfig.CLIENT_PORTS.items():
                    if port2 == appendEntryMessage.receiver:
                        print(str(id2).upper()+" is down")
            else:
                for id, port in serverConfig.SERVER_PORTS.items():
                    if port == appendEntryMessage.receiver:
                        print(str(id).upper()+" is down")
