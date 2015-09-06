class player(object):
    """docstring for player"""
    def __init__(self, arg):
        super(player, self).__init__()
        self.arg = arg
        
    def make_move( self ):
        raise NotImplementedError( "This is an abstract class - this method have to be implemented" )
