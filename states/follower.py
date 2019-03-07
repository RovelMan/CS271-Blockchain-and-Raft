from server import *
from messages.requestVote import RequestVoteResponse
import socket
import serverConfig

class Follower:

    def __init__(self):
        self.voteGiven = False
        #self.timeout  = timeout

    def respondToRequestVote(self, server, voteRequest):
        print("---My server id: -- "+ str(server.id))
        if (server.currentTerm < voteRequest.currentTerm and not self.voteGiven):
            self.voteGiven = True
            voteResponse = RequestVoteResponse(
            voteRequest.currentTerm, server.id, serverConfig.SERVER_PORTS[voteRequest.sender], True)
            self.sendReqVoteResponseMessage(voteResponse)

    def sendReqVoteResponseMessage(self, reqVoteResponse):
        s = socket.socket()
        print("Sending REQUESTVOTERESPONSE message to " + str(reqVoteResponse.receiver))
        s.connect(("127.0.0.1", reqVoteResponse.receiver))
        dataString = pickle.dumps(reqVoteResponse)
        s.send(dataString)
        s.close()
