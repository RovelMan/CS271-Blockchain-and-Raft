#class Candidate:
from server import *
import socket

# def set_server_to_candidate(self, server):
#     self.server = server
#     self.votesreceived = {}
#     self.startElection()

def startElection(server):
    server.currentTerm += 1
    print("Candidate updated term to " + str(server.currentTerm))
    sender = server.id
    for recID in serverPorts.keys():
        if (recID != sender):
            reqVoteMsg = RequestVote(
            server.currentTerm, sender, serverPorts[recID], server.id, server.lastLogIndex, server.lastLogTerm)
            sendReqVoteMessage(reqVoteMsg)
    print("Election Begun")

def sendReqVoteMessage(reqVoteMsg):
    # s1 = socket.socket()
    # print("Sending STOP message to " + str(reqVoteMsg.receiver))
    # s1.connect(("127.0.0.1", reqVoteMsg.receiver))
    # s1.send("STOP")
    # s1.close()
    s = socket.socket()
    print("Sending REQUESTVOTE message to " + str(reqVoteMsg.receiver))
    s.connect(("127.0.0.1", reqVoteMsg.receiver))
    dataString = pickle.dumps(reqVoteMsg)
    s.send(dataString)
    s.close()

# def handleResponseVote(server, vote):
