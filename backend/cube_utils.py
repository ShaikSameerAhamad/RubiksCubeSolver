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

def convert_to_kociemba_format(cube_state: str) -> str:
    """
    Convert various cube state formats to Kociemba format
    
    Args:
        cube_state: Cube state in various possible formats
        
    Returns:
        Cube state in standard Kociemba format
    """
    # Remove whitespace and convert to uppercase
    cleaned = re.sub(r'\s+', '', cube_state.upper())
    
    # If already in correct format, return as-is
    if len(cleaned) == 54 and set(cleaned).issubset(set('UDLRFB')):
        return cleaned
    
    # Handle color name to letter mapping
    color_map = {
        'WHITE': 'U', 'W': 'U',
        'YELLOW': 'D', 'Y': 'D', 
        'RED': 'R', 'R': 'R',
        'ORANGE': 'L', 'O': 'L',
        'GREEN': 'F', 'G': 'F',
        'BLUE': 'B', 'B': 'B'
    }
    
    # Try to convert color names/abbreviations
    converted = cleaned
    for color, letter in color_map.items():
        converted = converted.replace(color, letter)
    
    return converted

def convert_from_kociemba_format(cube_state: str, output_format: str = 'colors') -> str:
    """
    Convert from Kociemba format to other formats
    
    Args:
        cube_state: Cube state in Kociemba format
        output_format: 'colors', 'numbers', or 'letters'
        
    Returns:
        Converted cube state string
    """
    if len(cube_state) != 54:
        raise ValueError("Invalid cube state length")
    
    if output_format == 'colors':
        color_map = {
            'U': 'White', 'D': 'Yellow',
            'R': 'Red', 'L': 'Orange', 
            'F': 'Green', 'B': 'Blue'
        }
        return ''.join(color_map.get(c, c) for c in cube_state)
    
    elif output_format == 'numbers':
        number_map = {
            'U': '1', 'D': '2', 'R': '3',
            'L': '4', 'F': '5', 'B': '6'
        }
        return ''.join(number_map.get(c, c) for c in cube_state)
    
    elif output_format == 'letters':
        return cube_state  # Already in letter format
    
    else:
        raise ValueError(f"Unknown output format: {output_format}")

def generate_scramble(num_moves: int = 20) -> Tuple[str, str]:
    """
    Generate a random scramble sequence and resulting cube state
    
    Args:
        num_moves: Number of moves in the scramble
        
    Returns:
        Tuple of (scramble_sequence, resulting_cube_state)
    """
    if num_moves < 1 or num_moves > 100:
        raise ValueError("Number of moves must be between 1 and 100")
    
    scramble_moves = []
    cube_state = SOLVED_CUBE
    
    prev_face = None
    prev_prev_face = None
    
    for _ in range(num_moves):
        # Get available moves (avoid redundant consecutive moves)
        available_moves = []
        
        for move in ALL_MOVES:
            face = move[0]  # Get the face letter (U, D, R, L, F, B)
            
            # Don't repeat the same face consecutively
            if face == prev_face:
                continue
                
            # Don't do opposite faces back-to-back-to-back
            if (prev_face and prev_prev_face and 
                face == prev_prev_face and 
                MOVE_OPPOSITES.get(prev_face) == face):
                continue
            
            available_moves.append(move)
        
        # Choose a random move
        move = random.choice(available_moves)
        scramble_moves.append(move)
        
        # Apply the move to the cube state
        cube_state = apply_move(cube_state, move)
        
        # Update previous faces
        prev_prev_face = prev_face
        prev_face = move[0]
    
    scramble_sequence = ' '.join(scramble_moves)
    return scramble_sequence, cube_state

def apply_move(cube_state: str, move: str) -> str:
    """
    Apply a single move to a cube state
    
    Args:
        cube_state: Current cube state (54 characters)
        move: Move to apply (e.g., 'U', 'R\'', 'F2')
        
    Returns:
        New cube state after applying the move
    """
    if len(cube_state) != 54:
        raise ValueError("Invalid cube state length")
    
    # Convert string to list for manipulation
    cube = list(cube_state)
    
    # Parse the move
    face = move[0]
    if len(move) == 1:
        rotations = 1  # Clockwise
    elif move.endswith('\''):
        rotations = 3  # Counter-clockwise (3 clockwise rotations)
    elif move.endswith('2'):
        rotations = 2  # 180 degrees
    else:
        raise ValueError(f"Invalid move format: {move}")
    
    # Apply the rotation the specified number of times
    for _ in range(rotations):
        cube = _rotate_face_clockwise(cube, face)
    
    return ''.join(cube)

def apply_move_sequence(cube_state: str, moves: str) -> str:
    """
    Apply a sequence of moves to a cube state
    
    Args:
        cube_state: Starting cube state
        moves: Space-separated sequence of moves
        
    Returns:
        Final cube state after all moves
    """
    current_state = cube_state
    
    if not moves.strip():
        return current_state
    
    move_list = moves.strip().split()
    
    for move in move_list:
        current_state = apply_move(current_state, move)
    
    return current_state

def _rotate_face_clockwise(cube: List[str], face: str) -> List[str]:
    """
    Rotate a face clockwise once, including adjacent edges
    
    Args:
        cube: List representation of cube state
        face: Face to rotate ('U', 'D', 'R', 'L', 'F', 'B')
        
    Returns:
        Updated cube list
    """
    cube = cube.copy()  # Don't modify the original
    
    if face == 'U':
        # Rotate the Up face itself
        _rotate_face_stickers(cube, [0, 1, 2, 5, 8, 7, 6, 3])
        
        # Rotate adjacent edges
        temp = [cube[18], cube[19], cube[20]]  # Front edge
        cube[18], cube[19], cube[20] = cube[9], cube[10], cube[11]    # Right -> Front
        cube[9], cube[10], cube[11] = cube[45], cube[46], cube[47]    # Back -> Right
        cube[45], cube[46], cube[47] = cube[36], cube[37], cube[38]   # Left -> Back
        cube[36], cube[37], cube[38] = temp[0], temp[1], temp[2]      # Front -> Left
        
    elif face == 'D':
        # Rotate the Down face itself
        _rotate_face_stickers(cube, [27, 28, 29, 32, 35, 34, 33, 30])
        
        # Rotate adjacent edges
        temp = [cube[24], cube[25], cube[26]]  # Front edge
        cube[24], cube[25], cube[26] = cube[42], cube[43], cube[44]   # Left -> Front
        cube[42], cube[43], cube[44] = cube[51], cube[52], cube[53]   # Back -> Left
        cube[51], cube[52], cube[53] = cube[15], cube[16], cube[17]   # Right -> Back
        cube[15], cube[16], cube[17] = temp[0], temp[1], temp[2]      # Front -> Right
        
    elif face == 'R':
        # Rotate the Right face itself
        _rotate_face_stickers(cube, [9, 10, 11, 14, 17, 16, 15, 12])
        
        # Rotate adjacent edges
        temp = [cube[2], cube[5], cube[8]]    # Up edge
        cube[2], cube[5], cube[8] = cube[20], cube[23], cube[26]      # Front -> Up
        cube[20], cube[23], cube[26] = cube[29], cube[32], cube[35]   # Down -> Front
        cube[29], cube[32], cube[35] = cube[47], cube[50], cube[53]   # Back -> Down
        cube[47], cube[50], cube[53] = temp[0], temp[1], temp[2]      # Up -> Back
    
    elif face == 'L':
        # Rotate the Left face itself
        _rotate_face_stickers(cube, [36, 37, 38, 41, 44, 43, 42, 39])
        
        # Rotate adjacent edges
        temp = [cube[0], cube[3], cube[6]]    # Up edge
        cube[0], cube[3], cube[6] = cube[45], cube[48], cube[51]      # Back -> Up
        cube[45], cube[48], cube[51] = cube[27], cube[30], cube[33]   # Down -> Back
        cube[27], cube[30], cube[33] = cube[18], cube[21], cube[24]   # Front -> Down
        cube[18], cube[21], cube[24] = temp[0], temp[1], temp[2]      # Up -> Front
    
    elif face == 'F':
        # Rotate the Front face itself
        _rotate_face_stickers(cube, [18, 19, 20, 23, 26, 25, 24, 21])
        
        # Rotate adjacent edges
        temp = [cube[6], cube[7], cube[8]]    # Up edge
        cube[6], cube[7], cube[8] = cube[44], cube[41], cube[38]      # Left -> Up (reversed)
        cube[44], cube[41], cube[38] = cube[33], cube[30], cube[27]   # Down -> Left (reversed)
        cube[33], cube[30], cube[27] = cube[9], cube[12], cube[15]    # Right -> Down (reversed)
        cube[9], cube[12], cube[15] = temp[0], temp[1], temp[2]       # Up -> Right
    
    elif face == 'B':
        # Rotate the Back face itself
        _rotate_face_stickers(cube, [45, 46, 47, 50, 53, 52, 51, 48])
        
        # Rotate adjacent edges
        temp = [cube[0], cube[1], cube[2]]    # Up edge
        cube[0], cube[1], cube[2] = cube[11], cube[14], cube[17]      # Right -> Up
        cube[11], cube[14], cube[17] = cube[35], cube[34], cube[33]   # Down -> Right (reversed)
        cube[35], cube[34], cube[33] = cube[42], cube[39], cube[36]   # Left -> Down (reversed)
        cube[42], cube[39], cube[36] = temp[0], temp[1], temp[2]      # Up -> Left
    
    return cube

def _rotate_face_stickers(cube: List[str], positions: List[int]) -> None:
    """
    Rotate the stickers on a face clockwise
    
    Args:
        cube: Cube state as list
        positions: List of positions in clockwise order (corners then edges)
    """
    # Get the face stickers in order: corners then edges
    temp = cube[positions[0]]
    
    # Rotate positions clockwise
    for i in range(len(positions) - 1):
        cube[positions[i]] = cube[positions[i + 1]]
    
    cube[positions[-1]] = temp

def get_move_sequence_length(moves: str) -> int:
    """
    Count the number of moves in a move sequence
    
    Args:
        moves: Space-separated move sequence
        
    Returns:
        Number of individual moves
    """
    if not moves.strip():
        return 0
    return len(moves.strip().split())

def reverse_move_sequence(moves: str) -> str:
    """
    Reverse a move sequence (useful for undoing scrambles)
    
    Args:
        moves: Original move sequence
        
    Returns:
        Reversed move sequence
    """
    if not moves.strip():
        return ""
    
    move_list = moves.strip().split()
    reversed_moves = []
    
    for move in reversed(move_list):
        reversed_moves.append(reverse_move(move))
    
    return ' '.join(reversed_moves)

def reverse_move(move: str) -> str:
    """
    Get the reverse of a single move
    
    Args:
        move: Single move (e.g., 'U', 'R\'', 'F2')
        
    Returns:
        Reverse move
    """
    if len(move) == 1:
        return move + '\''  # U -> U'
    elif move.endswith('\''):
        return move[0]      # U' -> U
    elif move.endswith('2'):
        return move         # U2 -> U2 (self-inverse)
    else:
        raise ValueError(f"Invalid move format: {move}")

def is_valid_move_sequence(moves: str) -> bool:
    """
    Check if a move sequence contains only valid moves
    
    Args:
        moves: Move sequence to validate
        
    Returns:
        True if all moves are valid
    """
    if not moves.strip():
        return True
    
    try:
        move_list = moves.strip().split()
        valid_moves = set(ALL_MOVES)
        
        for move in move_list:
            if move not in valid_moves:
                return False
        
        return True
        
    except Exception:
        return False

def optimize_move_sequence(moves: str) -> str:
    """
    Basic optimization of a move sequence by combining consecutive same-face moves
    
    Args:
        moves: Original move sequence
        
    Returns:
        Optimized move sequence
    """
    if not moves.strip():
        return ""
    
    move_list = moves.strip().split()
    optimized = []
    
    i = 0
    while i < len(move_list):
        current_move = move_list[i]
        face = current_move[0]
        
        # Collect all consecutive moves of the same face
        same_face_moves = [current_move]
        j = i + 1
        
        while j < len(move_list) and move_list[j][0] == face:
            same_face_moves.append(move_list[j])
            j += 1
        
        # Combine the moves
        combined = combine_same_face_moves(same_face_moves)
        if combined:
            optimized.append(combined)
        
        i = j
    
    return ' '.join(optimized)

def combine_same_face_moves(moves: List[str]) -> Optional[str]:
    """
    Combine multiple moves of the same face into a single move
    
    Args:
        moves: List of moves of the same face
        
    Returns:
        Combined move or None if they cancel out
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
    
    # Normalize to 0-3 range
    total_rotation = total_rotation % 4
    
    if total_rotation == 0:
        return None
    elif total_rotation == 1:
        return face
    elif total_rotation == 2:
        return face + '2'
    elif total_rotation == 3:
        return face + '\''

# Example usage and testing
if __name__ == "__main__":
    print("Testing cube utilities...")
    
    # Test scramble generation
    scramble, state = generate_scramble(15)
    print(f"Generated scramble: {scramble}")
    print(f"Resulting state: {state[:20]}...")
    
    # Test move application
    print(f"\nApplying 'U R U\' R\'' to solved cube:")
    result = apply_move_sequence(SOLVED_CUBE, "U R U' R'")
    print(f"Result: {result[:20]}...")
    
    # Test optimization
    test_moves = "U U U' R R2 R' F F F"
    optimized = optimize_move_sequence(test_moves)
    print(f"\nOriginal: {test_moves}")
    print(f"Optimized: {optimized}")
    
    # Test reverse
    reversed_moves = reverse_move_sequence("U R U' R'")
    print(f"\nReverse of 'U R U\\' R\\'': {reversed_moves}")