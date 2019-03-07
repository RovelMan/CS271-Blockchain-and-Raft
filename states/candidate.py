#class Candidate:
from server import *
import socket
from leader import Leader
import serverConfig

class Candidate:

    def __init__(self):
        self.votesReceived = []

    def startElection(self, server):
        server.currentTerm += 1
        print("Candidate updated term to " + str(server.currentTerm))
        sender = server.id
        for recID in serverConfig.SERVER_PORTS.keys():
            if (recID != sender):
                reqVoteMsg = RequestVote(
                    server.currentTerm, sender, serverConfig.SERVER_PORTS[recID], server.id, server.lastLogIndex, server.lastLogTerm
                )
                self.sendReqVoteMessage(reqVoteMsg)
        print("Election Begun")

    def sendReqVoteMessage(self, reqVoteMsg):
        s = socket.socket()
        print("Sending REQUESTVOTE message to " + str(reqVoteMsg.receiver))
        s.connect(("127.0.0.1", reqVoteMsg.receiver))
        dataString = pickle.dumps(reqVoteMsg)
        s.send(dataString)
        s.close()

    def handleResponseVote(self, server, vote):
        print("I got response vote from "+str(vote.sender))
        self.votesReceived.append(vote.sender)
        if (len(self.votesReceived) == 2):
            server.currentState = Leader()
            server.currentState.initiateLeader(server)
            print(" I am now leader")