import board
import random
from player import Player
import discord


class UrController:
    def __init__(self):
        w = 3
        h = 8
        self.board = board.Board(h, w)
        self.dice_roll = 0
        self.players = []
        self.players.append(Player("Player 1", "L"))
        self.players.append(Player("Player 2", "R"))
        self.turn = self.players[0]

    def get_turn(self):
        return self.turn

    def get_printed_board(self):
        display = self.board.to_text()
        return display

    def get_dice_roll(self):
        roll = self.get_dice_roll_helper()
        roll = roll + self.get_dice_roll_helper()
        roll = roll + self.get_dice_roll_helper()
        roll = roll + self.get_dice_roll_helper()
        return roll

    def get_dice_roll_helper(self):
        roll = random.randint(0, 4)
        if roll == 0 or roll == 2:
            return 1
        else:
            return 0

    def create_board(self):
        display = self.get_printed_board()

    async def handle_play_ur(self):
        board = self.create_board()
        return board, self.turn

    async def roll_dice(self):
        board = self.get_printed_board()
        dice_roll = self.get_dice_roll()
        moves = None
        self.dice_roll = dice_roll
        return board, dice_roll, moves, self.turn

    async def new_piece(self, message):
        """
        get the board
        get the current player
        get the dice roll
        move the piece from that player to the dice roll
        display the result
        """
        current_board = self.board
        current_player = self.turn
        current_dice_roll = self.dice_roll

        if len(current_player.tokens) < 1:
            raise Exception("new peice error. current_player.tokens < 1")

        current_board.place_token(current_player.tokens[0], current_dice_roll)

        board_string = self.get_printed_board()
        embedVar = discord.Embed(
            title="The Game of Ur", color=0x00FF00, type="rich", author="Pasha"
        )
        embedVar.add_field(name="Board", value=board_string, inline=True)
        embedVar.add_field(name="Turn", value=self.turn.name, inline=True)
        new_message = await message.channel.send(embed=embedVar)
        return new_message

    def update_turn(self):
        if self.turn == self.players[0]:
            self.turn = self.players[1]
        else:
            self.turn = self.players[0]
