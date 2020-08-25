"""This module helps check for valid moves in the context of a board."""

from nerdchess import pieces
from nerdchess.move import Move


class BoardRules():
    """Applies different boardrules.

    Parameters:
        move: The move to check against
        board: The board to check against

    Attributes:
        move: The move we're checking
        board: The board we're checking
        valid: Is the checked move valid? see self.apply()
        origin: The origin square of the move
        destination: The destination square of the move
        piece: The piece being moved
    """

    def __init__(self, move, board):
        """Init."""
        self.move = move
        self.board = board
        self.valid = True
        (self.origin,
         self.destination) = self.move.get_origin_destination(self.board)
        self.piece = self.origin.occupant
        self.apply()

    def apply(self):
        """Apply boardrules based on the moved piece."""
        if isinstance(self.piece, pieces.Pawn):
            self.__pawn_rules()
        if not isinstance(self.piece, pieces.Knight):
            self.__blocking_pieces()
        if self.move.is_castling(self.board):
            self.__castling()
        else:
            if self.move.is_capturing(self.board):
                self.__capturing()
            self.__self_checking()

    def __capturing(self):
        if self.destination.occupant.color == self.origin.occupant.color:
            self.valid = False

    def __pawn_rules(self):
        """Rules to apply to pawns only."""
        if self.move.horizontal == 1:
            # If we're going horizontal, are we at least capturing?
            if not self.destination.occupant:
                d_letter = self.move.destination[0]
                o_number = int(self.move.origin[1])
                # If not, is it at least en passant?
                if not isinstance(
                        self.board.squares[d_letter][o_number].occupant,
                        pieces.Pawn):
                    self.valid = False

    def __blocking_pieces(self):
        """Check if the move is being blocked."""
        for square in self.move.squares_between():
            c = square[0]
            i = int(square[1])
            if self.board.squares[c][i].occupant:
                self.valid = False

    def __self_checking(self):
        """Check if the move puts the player itself in check."""
        newboard = self.board.new_board(self.move)
        if newboard.is_check() == self.piece.color:
            self.valid = False

    def __castling(self):
        """Apply rules specific to castling."""
        pattern = []

        if self.board.is_check() == self.piece.color:
            self.valid = False

        if self.move.horizontal > 0:
            pattern = [
                (1, 0),
                (2, 0)
            ]
        else:
            pattern = [
                (-1, 0),
                (-2, 0)
            ]

        for move in pattern:
            inter_move = Move.from_position(self.piece.position, move)
            inter_board = self.board.new_board(inter_move)
            if inter_board.is_check() == self.piece.color:
                self.valid = False
