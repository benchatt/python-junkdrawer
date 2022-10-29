from dataclasses import dataclass
from enum import Enum
from typing import Union
import sys

#NOTE: implementing a 15x15 grid, not a 7x7 overlaid on an 8x8

class PieceType(Enum):
    GUERRILLA = 0
    COIN = 1

@dataclass
class Coordinate:
    x = int
    y = int

class Turn(Enum):
    GUERRILLA_START = 0
    GUERRILLA_MID = 1
    COIN_START = 2
    COIN_MID = 3

@dataclass
class PlayedPieces:
    guerrillas: int = 0
    coins: int = 6

@dataclass
class Piece:
    ptype: PieceType
    loc: Coordinate

@dataclass
class Move:
    piece_type: PieceType
    start: Coordinate
    end: Coordinate
    capture: bool

class GameState():
    def __init__(self, dim: int):
        self.dim = dim
        self.board = [[None] * dim] * dim
        self.turn: Turn = Turn.GUERRILLA_START
        self.active: Union[None, Coordinate] = None
        self.history: list[Move] = []
        self.pieces: PlayedPieces = PlayedPieces()
        self.bag: int = 60
        self.board_setup()

    def analyze_for_win(self) -> Union[None, PieceType]:
        if self.pieces.guerrillas == 0 or self.bag == 0:
            return PieceType.COIN
        if self.pieces.coins == 0:
            return PieceType.GUERRILLA

    def location_on_board(self, loc: Coordinate) -> bool:
        if (-1 < loc.x < self.dim) and (-1 < loc.y < self.dim):
            return True
        else:
            return False

    def contents_of_loc(self, loc: Coordinate) -> Union[None, Piece]:
        return self.board[loc.x][loc.y]

    def is_capturable_by(self, attacker: Piece, victim: Piece) -> bool:
        if victim.ptype == attacker.ptype:
            return False
        if victim.ptype == PieceType.GUERRILLA:
            diffx = victim.loc.x - attacker.loc.x
            diffy = victim.loc.y - attacker.loc.y
            if abs(diffx) != 1 or abs(diffy) != 1:
                return False
            landing = Coordinate(
                x = victim.loc.x + diffx,
                y = victim.loc.y + diffy
            )
            if not self.location_on_board(landing):
                return False
            if contents_of_loc(landing) is not None:
                return False
            return True
        if victim.ptype == PieceType.COIN:
            corner_dists = [[1,1],[-1,1],[1,-1],[-1,-1]]
            for addend in corner_dists:
                candidate = Coordinate(
                    x = victim.loc.x + addend[0],
                    y = victim.loc.y + addend[1]
                )
                if not self.location_on_board(candidate):
                    continue
                if candidate == attacker.loc:
                    continue
                if self.contents_of_loc(candidate).ptype == PieceType.GUERRILLA:
                    continue
                return False
            return True

    def board_setup(self):
        pass


def isEven(x: int) -> bool:
    return (x % 2) == 0

def isLegalPlace(pt: PieceType, loc: Coordinate) -> bool:
    if pt == PieceType.GUERRILLA:
        return (not isEven(loc.x)) and (not isEven(loc.y))
    elif pt == PieceType.COIN:
        return (isEven(loc.x) and isEven(loc.y)) and \
            (not isEven((loc.x + loc.y) / 2))
    else:
        sys.exit('Illegal piece type')

def isContiguous(pt: PieceType, a: Coordinate, b: Coordinate) -> bool:
    if pt == PieceType.GUERRILLA:
        return (a.x == b.x and abs(a.y - b.y) == 2) or \
            (abs(a.x - b.x) == 2 and a.y == b.y)
    elif pt == PieceType.COIN:
        return (abs(a.x - b.x) == 2 and abs(a.y - b.y) == 2)
    else:
        sys.exit('Illegal piece type')


