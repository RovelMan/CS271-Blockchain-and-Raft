from raftmessage import Message

class RequestVote(Message):
    def __init__(self, currentTerm, sender, receiver, candidateId, lastLogIndex, lastLogTerm):
        Message.__init__(self, currentTerm, sender, receiver)
        self.candidateId = candidateId
        self.lastLogIndex = lastLogIndex
        self.lastLogTerm = lastLogTerm


class RequestVoteResponse(Message):
    def __init__(self, currentTerm, sender, receiver, acceptVote):
        Message.__init__(self, curentTerm, sender, receiver)
        self.acceptVote = acceptVote
