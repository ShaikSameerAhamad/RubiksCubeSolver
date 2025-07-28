"""
Cube Utilities

This module provides utility functions for cube format conversion,
scramble generation, and cube state manipulation.
"""

import random
from typing import List, Tuple, Dict, Optional
import re

# Standard solved cube state in Kociemba format
SOLVED_CUBE = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"

# All possible moves in standard notation
ALL_MOVES = [
    'U', 'U\'', 'U2',    # Up face moves
    'D', 'D\'', 'D2',    # Down face moves
    'R', 'R\'', 'R2',    # Right face moves
    'L', 'L\'', 'L2',    # Left face moves
    'F', 'F\'', 'F2',    # Front face moves
    'B', 'B\'', 'B2'     # Back face moves
]

# Move opposites (for avoiding redundant moves in scrambles)
MOVE_OPPOSITES = {
    'U': 'D', 'D': 'U',
    'R': 'L', 'L': 'R',
    'F': 'B', 'B': 'F'
}

# --- UNTOUCHED ORIGINAL FUNCTIONS ---

def convert_to_kociemba_format(cube_state: str) -> str:
    """
    Convert various cube state formats to Kociemba format
    """
    cleaned = re.sub(r'\s+', '', cube_state.upper())
    if len(cleaned) == 54 and set(cleaned).issubset(set('UDLRFB')):
        return cleaned
    color_map = {
        'WHITE': 'U', 'W': 'U', 'YELLOW': 'D', 'Y': 'D', 'RED': 'R',
        'ORANGE': 'L', 'O': 'L', 'GREEN': 'F', 'G': 'F', 'BLUE': 'B',
    }
    converted = cleaned
    for color, letter in color_map.items():
        converted = converted.replace(color, letter)
    return converted

def convert_from_kociemba_format(cube_state: str, output_format: str = 'colors') -> str:
    """
    Convert from Kociemba format to other formats
    """
    if len(cube_state) != 54:
        raise ValueError("Invalid cube state length")
    if output_format == 'colors':
        color_map = {'U': 'White', 'D': 'Yellow', 'R': 'Red', 'L': 'Orange', 'F': 'Green', 'B': 'Blue'}
        return ''.join(color_map.get(c, c) for c in cube_state)
    elif output_format == 'numbers':
        number_map = {'U': '1', 'D': '2', 'R': '3', 'L': '4', 'F': '5', 'B': '6'}
        return ''.join(number_map.get(c, c) for c in cube_state)
    elif output_format == 'letters':
        return cube_state
    else:
        raise ValueError(f"Unknown output format: {output_format}")

# --- BUG FIX: NEW, CORRECT MOVE LOGIC ---

# Sticker indices for each face's cycle (clockwise)
FACE_CYCLES = {
    'U': [0, 2, 8, 6, 1, 5, 7, 3],
    'R': [9, 11, 17, 15, 10, 14, 16, 12],
    'F': [18, 20, 26, 24, 19, 23, 25, 21],
    'D': [27, 29, 35, 33, 28, 32, 34, 30],
    'L': [36, 38, 44, 42, 37, 41, 43, 39],
    'B': [45, 47, 53, 51, 46, 50, 52, 48],
}

# Sticker indices for adjacent side cycles for each move (clockwise)
ADJACENT_CYCLES = {
    'U': [18, 9, 45, 36, 19, 10, 46, 37, 20, 11, 47, 38],
    'R': [8, 26, 35, 51, 5, 23, 32, 48, 2, 20, 29, 45],
    'F': [8, 15, 33, 44, 7, 12, 30, 41, 6, 9, 27, 38],
    'D': [26, 53, 44, 17, 25, 52, 43, 16, 24, 51, 42, 15],
    'L': [6, 24, 33, 53, 3, 21, 30, 50, 0, 18, 27, 47],
    'B': [2, 17, 35, 42, 1, 14, 34, 39, 0, 9, 29, 36],
}

def _cycle_stickers(state: List[str], cycle: List[int], rotations: int = 1):
    """Helper function to perform a cyclic permutation on a list of stickers."""
    for _ in range(rotations):
        last_val = state[cycle[-1]]
        for i in range(len(cycle) - 1, 0, -1):
            state[cycle[i]] = state[cycle[i-1]]
        state[cycle[0]] = last_val

def apply_move(cube_state: str, move: str) -> str:
    """
    Apply a single move to a cube state using a robust cycle-based method.
    """
    state = list(cube_state)
    face = move[0]
    
    if len(move) > 1 and move[1] == "'":
        rotations = 3
    elif len(move) > 1 and move[1] == '2':
        rotations = 2
    else:
        rotations = 1

    # Rotate face stickers
    _cycle_stickers(state, FACE_CYCLES[face], rotations)
    
    # Rotate adjacent stickers (three cycles of four)
    adj = ADJACENT_CYCLES[face]
    _cycle_stickers(state, [adj[0], adj[1], adj[2], adj[3]], rotations)
    _cycle_stickers(state, [adj[4], adj[5], adj[6], adj[7]], rotations)
    _cycle_stickers(state, [adj[8], adj[9], adj[10], adj[11]], rotations)
    
    return "".join(state)

# --- UNTOUCHED ORIGINAL FUNCTIONS (that now use the new apply_move) ---

def generate_scramble(num_moves: int = 20) -> Tuple[str, str]:
    """
    Generate a random scramble sequence and resulting cube state.
    """
    if not 1 <= num_moves <= 100:
        raise ValueError("Number of moves must be between 1 and 100")
    scramble_moves = []
    last_face = None
    for _ in range(num_moves):
        while True:
            move = random.choice(ALL_MOVES)
            current_face = move[0]
            if current_face != last_face and MOVE_OPPOSITES.get(current_face) != last_face:
                scramble_moves.append(move)
                last_face = current_face
                break
    scramble_sequence = ' '.join(scramble_moves)
    scrambled_state = apply_move_sequence(SOLVED_CUBE, scramble_sequence)
    return scramble_sequence, scrambled_state

def apply_move_sequence(cube_state: str, moves: str) -> str:
    """
    Apply a sequence of moves to a cube state.
    """
    current_state = cube_state
    if not moves.strip():
        return current_state
    for move in moves.strip().split():
        current_state = apply_move(current_state, move)
    return current_state

def get_move_sequence_length(moves: str) -> int:
    """
    Count the number of moves in a move sequence.
    """
    if not moves.strip():
        return 0
    return len(moves.strip().split())

def reverse_move_sequence(moves: str) -> str:
    """
    Reverse a move sequence (useful for undoing scrambles).
    """
    if not moves.strip():
        return ""
    move_list = moves.strip().split()
    reversed_moves = [reverse_move(move) for move in reversed(move_list)]
    return ' '.join(reversed_moves)

def reverse_move(move: str) -> str:
    """
    Get the reverse of a single move.
    """
    if len(move) == 1:
        return move + '\''
    elif move.endswith('\''):
        return move[0]
    elif move.endswith('2'):
        return move
    else:
        raise ValueError(f"Invalid move format: {move}")

def is_valid_move_sequence(moves: str) -> bool:
    """
    Check if a move sequence contains only valid moves.
    """
    if not moves.strip():
        return True
    return all(move in ALL_MOVES for move in moves.strip().split())

def optimize_move_sequence(moves: str) -> str:
    """
    Basic optimization of a move sequence by combining consecutive same-face moves.
    """
    if not moves.strip():
        return ""
    move_list = moves.strip().split()
    optimized = []
    i = 0
    while i < len(move_list):
        face = move_list[i][0]
        same_face_moves = [move_list[i]]
        j = i + 1
        while j < len(move_list) and move_list[j][0] == face:
            same_face_moves.append(move_list[j])
            j += 1
        combined = combine_same_face_moves(same_face_moves)
        if combined:
            optimized.append(combined)
        i = j
    return ' '.join(optimized)

def combine_same_face_moves(moves: List[str]) -> Optional[str]:
    """
    Combine multiple moves of the same face into a single move.
    """
    if not moves:
        return None
    face = moves[0][0]
    total_rotation = 0
    for move in moves:
        if move == face:
            total_rotation += 1
        elif move == face + '\'':
            total_rotation -= 1
        elif move == face + '2':
            total_rotation += 2
    total_rotation %= 4
    if total_rotation == 0:
        return None
    elif total_rotation == 1:
        return face
    elif total_rotation == 2:
        return face + '2'
    elif total_rotation == 3:
        return face + '\''

if __name__ == "__main__":
    print("Testing cube utilities...")
    scramble, state = generate_scramble(20)
    print(f"Generated scramble: {scramble}")
    print(f"Resulting state: {state}")
    optimized = optimize_move_sequence("U U U' R R2 R'")
    print(f"Optimized 'U U U' R R2 R'': {optimized}")