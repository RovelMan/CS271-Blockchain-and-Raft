from raftMessage import Message

class ServerToClient(Message):
    def __init__(self, currentTerm, sender, receiver, leaderPort):
        Message.__init__(self, currentTerm, sender, receiver)
        self.leaderPort = leaderPort
