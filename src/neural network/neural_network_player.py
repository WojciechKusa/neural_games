import game.player
import neural_network




class NeuralNetworkPlayer(Player):
    """docstring for NeuralNetworkPlayer"""
    def __init__(self, arg):
        super(NeuralNetworkPlayer, self).__init__()
        self.arg = arg
    
    def make_move(self, board):
        self.board = board

        return 0