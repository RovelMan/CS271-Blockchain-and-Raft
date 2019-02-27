class Message:

    messageType = {
    "AppendEntry" : 0,
    "RequestVote" : 1,
    "ResponseRequestVote" : 2,
    "ResponseClient": 3
    }

    def __init__(self, currentTerm, sender, receiver):
        self.currentTerm = currentTerm
        self.sender = sender
        self.receiver = receiver
        self.data = data
