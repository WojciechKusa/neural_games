from network import Network

class Player(object):

    def __init__(self, type):
      super(Player, self).__init__()
      self.type = type # 0 - human, 1 - computer
      self.net = None

    def prepare(self, filename, ahead):
    	self.net = Network(filename, ahead)
    	self.net.train()
        
    def make_move(self, position):
    	response = self.net.sim(position)
    	return response[0][0]
