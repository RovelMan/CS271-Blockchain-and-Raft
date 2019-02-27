from raftmessage import Message

class RequestVote:
    def __init__(self, currentTerm, sender, receiver, candidateId, lastLogIndex, lastLogTerm):
        Message.__init__(self, currentTerm, sender, receiver)
        self.candidateId = candidateId
        self.lastLogIndex = lastLogIndex
        self.lastLogTerm = lastLogTerm


class RequestVoteResponse:
    def __init__(self, currentTerm, sender, receiver, acceptVote):
        Message.__init__(self, currentTerm, sender, receiver)
        self.acceptVote = acceptVote
