import sys
import socket

class Client(object):

  def __init__(self, id):
    if ((id != 'a') and (id != 'b') and (id != 'c')):
      print("Error! Invalid Client ID \nHas to be a, b or c \nQuitting...")
      return
    self._id = id
    print("Setup for Client" + id.upper() + " done!")

if __name__ == '__main__':
  clientA = Client('a')
  clientB = Client('b')
  clientC = Client('c')
