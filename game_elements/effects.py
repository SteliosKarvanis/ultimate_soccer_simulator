from game_elements.player import Player

class AbstractEffect:

    def __init__(self, player: Player):
        self.original_state = 0
        raise NotImplementedError(
            "This method is abstract and must be implemented in derived classes"
        )
    
    def transform(self, player: Player):
        raise NotImplementedError(
            "This method is abstract and must be implemented in derived classes"
        )

    def restore(self, player: Player):
        raise NotImplementedError(
            "This method is abstract and must be implemented in derived classes"
        )
    
class IncreaseSpeed(AbstractEffect):

    def __init__(self, player: Player):
        self.original_state = player.base_vel

    def transform(self, player: Player):
        player.base_vel *= 2
        player.angular_speed = player.base_vel*500

    def restore(self, player: Player):
        player.base_vel = self.original_state
        player.angular_speed = player.base_vel*500

class IncreaseSize(AbstractEffect):

    def __init__(self, player: Player):
        self.original_state = player.size

    def transform(self, player: Player):
        player.size = (self.original_state[0]*2, self.original_state[1]*2)

    def restore(self, player: Player):
        player.size = self.original_state


