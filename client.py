import sys, socket, pickle

class Client(object):

  def __init__(self, id):
    if ((id != 'a') and (id != 'b') and (id != 'c')):
      print("Error! Invalid Client ID \nHas to be a, b or c \nQuitting...")
      return
    self._id = id
    print("Setup for Client" + id.upper() + " done!")

if __name__ == '__main__':
  # clientA = Client('a')
  # clientB = Client('b')
  # clientC = Client('c')

  command = ''
  while command != 'q': 
    print("Commands:")
    print("\tMake transaction: m")
    print("\tQuit: q")
    command = raw_input("Enter command: ")
    if command == 'q':
      print("Quitting")
    elif command == 'm':
      reciever = raw_input("To whom? (b or c) ")
      amount = raw_input("How much? ")
      try:
        s = socket.socket()
        print("Sending transaction to " + str(7100))
        s.connect(("127.0.0.1", 7100))
        s.send(pickle.dumps("A " + str(reciever).upper() + " " + str(amount)))
        s.close()
      except:
        print("Server" + 'x'.upper() + " is down!")
    else:
      print("Invalid command! Try again...")
      
