class Player(object):
    """docstring for Player"""
    def __init__(self, type):
        super(Player, self).__init__()
        self.type = type # 0 - human, 1 - computer
        
    def make_move( self, board ):
        raise NotImplementedError( "This is an abstract class - this method have to be implemented" )

