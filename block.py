from square import Square, Color
from enum import Enum
import random
import copy

class BlockType(Enum):  
    I = "i"
    J = "j"
    L = "l"
    O = "o"
    S = "s"
    T = "t"
    Z = "z"
    
    @classmethod
    def get_random_block_type(cls):
        return random.choice(list(cls))

class Block:
    def __init__(self, block_type: BlockType = None, x: int = 0, y: int = 0, squares: list[Square] = None):
        self.squares = squares or self._create_block_shape(block_type, x, y)
        self.block_type = block_type
      
    
    def _create_block_shape(self, block_type: BlockType, x: int, y: int) -> list[Square]:

        shapes = {
            BlockType.I: [
                (0, -1), (0, 0), (0, 1), (0, 2)  # Vertical line
            ],
            BlockType.J: [
                (-1, -1), (-1, 0), (0, 0), (1, 0)  # L-shape pointing right
            ],
            BlockType.L: [
                (1, -1), (-1, 0), (0, 0), (1, 0)  # L-shape pointing left
            ],
            BlockType.O: [
                (0, 0), (1, 0), (0, 1), (1, 1)  # 2x2 square
            ],
            BlockType.S: [
                (-1, 0), (0, 0), (0, 1), (1, 1)  # S-shape
            ],
            BlockType.T: [
                (0, -1), (-1, 0), (0, 0), (1, 0)  # T-shape
            ],
            BlockType.Z: [
                (-1, 1), (0, 1), (0, 0), (1, 0)  # Z-shape
            ]
        }
        
        colors = {
            BlockType.I: Color.BLUE,
            BlockType.J: Color.BLUE,
            BlockType.L: Color.RED,
            BlockType.O: Color.GREEN,
            BlockType.S: Color.GREEN,
            BlockType.T: Color.RED,
            BlockType.Z: Color.RED
        }
        
        relative_positions = shapes.get(block_type, [])
        color = colors.get(block_type, Color.BLUE)
        
        squares = []
        for rel_x, rel_y in relative_positions:
            squares.append(Square(color=color, x=x + rel_x, y=y + rel_y))
        
        return squares

    def get_squares(self):
        return self.squares

    def get_lowest_squares(self) -> int | None:
        if not self.squares:
            return None

        return max(square.y for square in self.squares)

    def move_left(self):
        for square in self.squares:
            square.x -= 1

    def move_right(self):
        for square in self.squares:
            square.x += 1


    def can_perform(self, squares: list[Square],width: int,operation_name: str):
        def is_in_wall(block: Block):
            return any(square.x < 0 or square.x >= width for square in block.squares)

        def is_in_other_block(block: Block):
            return any(
                block_square.x == square.x and block_square.y == square.y
                for block_square in block.squares
                for square in squares
            )

        block = Block(squares=copy.deepcopy(self.squares))
        method = getattr(block, operation_name) 
        method()

        _is_in_wall = is_in_wall(block)
        _is_in_other_block = is_in_other_block(block)

        return not _is_in_wall and not _is_in_other_block

    def rotate_left(self):
        self._rotate(clockwise=False)

    def rotate_right(self):
        self._rotate(clockwise=True)

    def _rotate(self, clockwise: bool):
        if self.block_type == BlockType.O or not self.squares:
            return
        
        avg_x = sum(square.x for square in self.squares) / len(self.squares)
        avg_y = sum(square.y for square in self.squares) / len(self.squares)
        
        pivot_x = round(avg_x)
        pivot_y = round(avg_y)
        
        for square in self.squares:
            rel_x = square.x - pivot_x
            rel_y = square.y - pivot_y
            
            if clockwise:
                new_rel_x = -rel_y
                new_rel_y = rel_x
            else:
                new_rel_x = rel_y
                new_rel_y = -rel_x
            
            square.x = pivot_x + new_rel_x
            square.y = pivot_y + new_rel_y

    def fall(self):
        for square in self.squares:
            square.y += 1

    
        

    def _is_on_floor(self, height: int):
        return any(square.y >= height - 1 for square in self.squares)

    def _is_on_other_block(self, squares: list[Square]):
        return any(
            s.x == square.x and s.y - 1 == square.y 
            for s in squares
            for square in self.squares
        )

    def fall_conditions_met(self, height: int, squares: list[Square]):
        return self._is_on_floor(height) or self._is_on_other_block(squares)
    
    def set_squares(self, squares: list[Square]):
        self.squares = squares

    def get_square(self, x: int, y: int):
        return self.squares[x][y]