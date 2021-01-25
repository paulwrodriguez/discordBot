from player_token import Player_Token


class Player:
    def __init__(self, name, symbol):

        self.token_count = 7
        self.tokens = []
        self.name = name
        for i in range(0, self.token_count):
            self.tokens.append(Player_Token(name, symbol))

        pass

    def get_token(self):
        if len(self.tokens) < 1:
            return None
        return self.tokens[0]

