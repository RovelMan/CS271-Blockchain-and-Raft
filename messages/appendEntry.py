from raftmessage import Message

class AppendEntry(Message):
    def __init__(self,  term, sender, receiver, leaderId, prevLogTerm, prevLogIndex, entries, commitIndex):
        Message.__init__(self, term, sender, receiver)
        self.msgtype = Message.messageType['AppendEntry']
        self.leaderId = leaderId
        self.prevLogTerm = prevLogTerm
        self.prevLogIndex = prevLogIndex
        self.entries = entries
        self.commitIndex = commitIndex
