from square import Square
from action import Tick, Action
from block import BlockType, Block


CLEAR_LINE_STOP_COUNTER = 100

class Game:
    def __init__(self,width: int, height: int):
        self.width = width
        self.height = height
        self.squares: list[Square] = []
        self.lines_to_clear: list[int] = []
        self.stopped_counter: int = 0

        self.block = self._create_new_block()



    def perform_tick(self, tick: Tick):
        # If the game is stopped, beacuse of line clear, do not perform any actions
        if self.stopped_counter > 0:
            self.stopped_counter -= 1
            return

        self._clear_lines_if_possible()

        # revive the block 
        if self.block is None:
            self.block = self._create_new_block()
            tick.reset_timer()
        self.lines_to_clear = []


        #choose the action to perform
        action = tick.get_action()
        if action is None or self.block is None:
            return
        if action is Action.MOVE_LEFT:
            self._move_left()
        elif action == Action.MOVE_RIGHT:
            self._move_right()
        elif action == Action.ROTATE_LEFT:
            self._rotate_left()
        elif action == Action.ROTATE_RIGHT:
            self._rotate_right()
        elif action == Action.FALL:
            self._fall()
        elif action == Action.DROP:
            self._drop()

        # check if any lines are full and clear them
        for line in range(self.height) :
            if self._can_clear_line(line):
                self.lines_to_clear.append(line)

            

        

    def _move_left(self):
        if not self.block.can_perform(self.squares, self.width, "move_left"):
            return
        self.block.move_left()

    def _move_right(self):
        if not self.block.can_perform(self.squares, self.width, "move_right"):
            return
        self.block.move_right()

    def _rotate_left(self):
        if not self.block.can_perform(self.squares, self.width, "rotate_left"):
            return
        self.block.rotate_left()

    def _rotate_right(self):
        if not self.block.can_perform(self.squares, self.width, "rotate_right"):
            return
        self.block.rotate_right()

    def _drop(self):
        self._fall()

    def _add_block_to_matrix(self):
        squares_from_block = self.block.get_squares()
        self.squares.extend(squares_from_block)
        self.block = None


    def _fall(self):
        if self.block.fall_conditions_met(self.height, self.squares):
            self._add_block_to_matrix()
            return
        self.block.fall()

    

    def _create_new_block(self):
        block_type = BlockType.get_random_block_type()
        return Block(
            block_type=block_type, 
            x=self.width//2, 
            y=0
        )


        
        


    def _can_clear_line(self, line: int):
        line_squares = list(filter(lambda square: square.y == line, self.squares))
        return  len(line_squares) == self.width

    def _clear_lines_if_possible(self):
        if not self.lines_to_clear:
            return


        squares_to_remove = []
        for square in self.squares:
            if square.y in self.lines_to_clear:
                squares_to_remove.append(square)
            elif square.y < min(self.lines_to_clear):
                square.y += len(self.lines_to_clear)

        for square in squares_to_remove:
            self.squares.remove(square)

        self.stopped_counter = CLEAR_LINE_STOP_COUNTER

    def is_game_over(self):
        return self.block is not None \
            and (self.block.fall_conditions_met(self.height, self.squares) \
            and self.block.get_lowest_squares() == 0)
        

    def get_all_squares(self):
        squares = list(self.squares)
        if self.block is not None:
            squares.extend(self.block.get_squares())
        return squares

    def get_lines_to_clear(self):
        return self.lines_to_clear




    