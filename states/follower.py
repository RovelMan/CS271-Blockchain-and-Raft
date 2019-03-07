# class Follower:
#
#     def __init__(self, timeout):
#         self.timeout  = timeout

def respondToRequestVote(server, voteRequest):
    if (server.currentTerm < voteRequest.currentTerm):
        voteResponse = RequestVoteResponse(
        voteRequest.currentTerm, server.id, voteRequest.sender, True)
