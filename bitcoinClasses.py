class Block:
    def __init__(self, header, txns):
        self.header = header
        self.txns = txns

class Header:
    def __init__(self, currentTerm, hashPrev, hashTxns, nonce):
        self.currentTerm = currentTerm
        self.hashPrev = hashPrev
        self.hashTxns = hashTxns
        self.nonce = nonce
