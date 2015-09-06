import player

class Game(object):
    """docstring for Game"""
    def __init__(self, arg):
        super(Game, self).__init__()
        self.arg = arg

    def start( self ):
        raise NotImplementedError( "This is an abstract class - this method have to be implemented" )


    def play( self ):
        self.generate_board()

        for player in players:
            player.make_move()

        self.step()

    gravity = 10
    moving_object = Moving()
    moving_object.moving = False
    moving_object.jumping = False
    

    def game_loop():
        if moving_object.jumping == False:
                    


    def draw_map():
        raise NotImplementedError( "This is an abstract class - this method have to be implemented" )

    def pause( self ):
        raise NotImplementedError( "This is an abstract class - this method have to be implemented" )

    def step( self ):
        raise NotImplementedError( "This is an abstract class - this method have to be implemented" )

    def stop( self ):
        raise NotImplementedError( "This is an abstract class - this method have to be implemented" )

    def reset( self ):
        raise NotImplementedError( "This is an abstract class - this method have to be implemented" )

    def generate_board( self ):
        raise NotImplementedError( "This is an abstract class - this method have to be implemented" )



