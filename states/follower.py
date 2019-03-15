from server import *
from messages.requestVote import RequestVoteResponse
import socket
import serverConfig

class Follower:

    def __init__(self):
        self.voteGiven = False

    def respondToRequestVote(self, server, voteRequest):
        # print("---My server id: -- "+ str(server.id))
        if (server.currentTerm < voteRequest.currentTerm and not self.voteGiven):
            self.voteGiven = True
            voteResponse = RequestVoteResponse(
            voteRequest.currentTerm, server.id, serverConfig.SERVER_PORTS[voteRequest.sender], True)
            self.sendReqVoteResponseMessage(voteResponse)

    def sendReqVoteResponseMessage(self, reqVoteResponse):
        try:
            s = socket.socket()
            print("Sending REQUESTVOTERESPONSE message to " + str(reqVoteResponse.receiver))
            s.connect(("127.0.0.1", reqVoteResponse.receiver))
            dataString = pickle.dumps(reqVoteResponse)
            s.send(dataString)
            s.close()
        except socket.error as e:
            for id, port in serverConfig.SERVER_PORTS.items():
                if port == reqVoteResponse.receiver:
                    print(str(id).upper()+" is down")
    
    def sendAcceptEntryResponseMessage(self, acceptEntryResponse):
        try:
            s = socket.socket()
            # print("Sending ACCEPTENTRYRESPONSE " + str(acceptEntryResponse.acceptEntry) + " message to " + str(acceptEntryResponse.receiver))
            s.connect(("127.0.0.1", acceptEntryResponse.receiver))
            dataString = pickle.dumps(acceptEntryResponse)
            s.send(dataString)
            s.close()
        except socket.error as e:
            for id, port in serverConfig.SERVER_PORTS.items():
                if port == acceptEntryResponse.receiver:
                    print(str(id).upper()+" is down")

    def answerLeader(self, server, data):
        acceptEntryResponse = None
        server.currentState = Follower()
        server.currentInterval = random.randint(12,15)
        server.currentTerm = data.currentTerm
        # print(server.lastLogIndex, data.prevLogIndex)
        if server.lastLogIndex != data.prevLogIndex:
            acceptEntryResponse = AcceptAppendEntry(
                server.currentTerm, server.id, serverConfig.SERVER_PORTS[data.sender], False
            )
            print("INCONSISTENT BLOCKCHAIN")
        else:
            acceptEntryResponse = AcceptAppendEntry(
                server.currentTerm, server.id, serverConfig.SERVER_PORTS[data.sender], True
            )
            if(data.entries == []):
                print("Got HEARTBEAT")
            else:
                server.lastLogIndex = len(server.blockchain) + 1
                server.blockchain.append(data.entries[0])
                print("Got a new BLOCK")
                server.tempTxns = []
        self.sendAcceptEntryResponseMessage(acceptEntryResponse)
            