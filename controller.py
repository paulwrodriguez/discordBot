import board
import random
from player import Player
import discord

game_die = "\U0001f3b2"
new_piece = "\U0001f4e4"
end_turn_emoji = "\U0001f51a"
one_emoji = '\U00000031'

move_piece_dict = {
    0 : new_piece,
    1 : '1\N{COMBINING ENCLOSING KEYCAP}',
    2 : '2\N{COMBINING ENCLOSING KEYCAP}',
    3 : '3\N{COMBINING ENCLOSING KEYCAP}',
    4 : '4\N{COMBINING ENCLOSING KEYCAP}',
    5 : '5\N{COMBINING ENCLOSING KEYCAP}',
    6 : '6\N{COMBINING ENCLOSING KEYCAP}',
    7 : '7\N{COMBINING ENCLOSING KEYCAP}',
}


class UrController:
    def __init__(self):
        w = 3
        h = 8
        self.board = board.Board(h, w)
        self.dice_roll = None
        self.players = []
        self.players.append(Player("Player 1", "L"))
        self.players.append(Player("Player 2", "R"))
        self.turn = self.players[0]

    def get_turn(self):
        return self.turn

    def get_printed_board(self):
        display = self.board.to_text()
        return display

    async def send_board_message(self,message, moves, add_dice = False):
        embedVar = discord.Embed(
            title="The Game of Ur", color=0x00FF00, type="rich", author="Pasha"
        )
        embedVar.add_field(name="Board", value=self.get_printed_board(), inline=True)
        embedVar.add_field(name="Turn", value=self.turn.name, inline=True)
        embedVar.add_field(name="Dice Roll", value=self.dice_roll, inline=True)
        new_message = await message.channel.send(embed=embedVar)

        if self.dice_roll == 0:
            await new_message.add_reaction(end_turn_emoji)
        if len(moves) == 0 and add_dice == False:
            await new_message.add_reaction(end_turn_emoji)
        elif len(moves) > 0: 
            for m in moves: 
                await new_message.add_reaction(move_piece_dict[m])

        if add_dice : 
            await new_message.add_reaction(game_die)

        return new_message


    async def handle_dice_roll(self,message):
        # get the dice Roll
        self.dice_roll = self.get_dice_roll()
        
        # find all the players peices that are on the board
        location_list = []
        location_list.append(0) # this is to handle moving a piece from home
        location_list = location_list + self.board.find_all_player_locations(self.turn.get_token())
        return_list = []
        # check if the piece can move
        if len(location_list) != 0 :
            token = self.turn.get_token()
            for index,value in enumerate(location_list):   
                # if it can move then add that piece to the list of moves
                if self.board.place_token_is_valid(token, value + self.dice_roll):
                    return_list.append(index)


        # send the print the board
        new_message = await self.send_board_message(message, return_list)
        print(return_list)
        return new_message

        


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

    async def handle_play_ur(self, message):
        new_message = await self.send_board_message(message, [], add_dice=True)
        return new_message

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

        current_board.place_token(current_player.get_token(), current_dice_roll)

        return await self.send_board_message(message, [])
    

    def update_turn(self):
        if self.turn == self.players[0]:
            self.turn = self.players[1]
        else:
            self.turn = self.players[0]

    async def handle_move_piece(self, reaction):
        message = reaction.message
        token = self.turn.get_token()
        current_location = 0

        for k,v in move_piece_dict.items():
            if v == reaction.emoji:
                current_location = k
                break
        
        location_list = self.board.find_all_player_locations(token)

        location = location_list[current_location-1]

        self.board.place_token(token, location + self.dice_roll)

        # reset token location 
        self.board.reset_tile(token , location)

        new_message = await self.send_board_message(message, [])
        return new_message



    async def handle_end_turn(self, message):

        self.update_turn()
        self.dice_roll = None

        new_message = await self.send_board_message(message, [], add_dice = True)
        

        return new_message