"""
Rubik's Cube Solver using Kociemba's Two-Phase Algorithm

This module provides functions to solve a Rubik's cube using the kociemba library,
which implements Kociemba's Two-Phase Algorithm for optimal solving.
"""

import kociemba
import time
from typing import Optional, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SolverError(Exception):
    """Custom exception for solver-related errors"""
    pass

def solve_cube(cube_state: str, max_depth: int = 24, timeout: int = 30) -> str:
    """
    Solve a Rubik's cube using Kociemba's Two-Phase Algorithm
    
    Args:
        cube_state: 54-character string representing the cube in Kociemba format
                   Each position represents a facelet:
                   - Positions 0-8: Up face (U)
                   - Positions 9-17: Right face (R) 
                   - Positions 18-26: Front face (F)
                   - Positions 27-35: Down face (D)
                   - Positions 36-44: Left face (L)
                   - Positions 45-53: Back face (B)
        max_depth: Maximum number of moves to search (default: 24)
        timeout: Maximum time in seconds to spend solving (default: 30)
    
    Returns:
        String containing the solution move sequence
        
    Raises:
        SolverError: If the cube cannot be solved or is invalid
    """
    try:
        # Validate input length
        if len(cube_state) != 54:
            raise SolverError(f"Cube state must be exactly 54 characters, got {len(cube_state)}")
        
        # Validate characters (should only contain U, D, L, R, F, B)
        valid_chars = set('UDLRFB')
        if not set(cube_state).issubset(valid_chars):
            invalid_chars = set(cube_state) - valid_chars
            raise SolverError(f"Invalid characters in cube state: {invalid_chars}")
        
        # Check if cube is already solved
        if is_solved(cube_state):
            logger.info("Cube is already solved!")
            return ""
        
        start_time = time.time()
        logger.info(f"Starting to solve cube with state: {cube_state[:20]}...")
        
        # Use kociemba to solve the cube
        try:
            solution = kociemba.solve(cube_state, max_depth=max_depth, timeout=timeout)
        except Exception as e:
            # Handle specific kociemba errors
            error_msg = str(e).lower()
            if "invalid" in error_msg or "unsolvable" in error_msg:
                raise SolverError(f"Invalid or unsolvable cube state: {e}")
            elif "timeout" in error_msg:
                raise SolverError(f"Solver timed out after {timeout} seconds")
            else:
                raise SolverError(f"Solver failed: {e}")
        
        solve_time = time.time() - start_time
        
        # Validate solution
        if solution is None:
            raise SolverError("Solver returned no solution")
        
        # Clean up the solution string
        solution = solution.strip()
        
        # Optimize the solution to remove redundant moves
        if solution:
            solution = optimize_solution(solution)
        
        # Log solution info
        move_count = len(solution.split()) if solution else 0
        logger.info(f"Cube solved in {solve_time:.3f}s with {move_count} moves: {solution}")
        
        return solution
        
    except SolverError:
        raise
    except Exception as e:
        raise SolverError(f"Unexpected error during solving: {e}")

def is_solved(cube_state: str) -> bool:
    """
    Check if a cube state represents a solved cube
    
    Args:
        cube_state: 54-character cube state string
        
    Returns:
        True if the cube is solved, False otherwise
    """
    try:
        # A solved cube has each face showing only one color
        # Face positions: U(0-8), R(9-17), F(18-26), D(27-35), L(36-44), B(45-53)
        faces = [
            cube_state[0:9],    # Up face
            cube_state[9:18],   # Right face  
            cube_state[18:27],  # Front face
            cube_state[27:36],  # Down face
            cube_state[36:45],  # Left face
            cube_state[45:54]   # Back face
        ]
        
        # Each face should have all identical characters
        for face in faces:
            if len(set(face)) != 1:
                return False
                
        return True
        
    except Exception:
        return False

def validate_kociemba_format(cube_state: str) -> Tuple[bool, str]:
    """
    Validate that a cube state is in proper Kociemba format
    
    Args:
        cube_state: 54-character cube state string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Check length
        if len(cube_state) != 54:
            return False, f"Length must be 54, got {len(cube_state)}"
        
        # Check valid characters
        valid_chars = set('UDLRFB')
        if not set(cube_state).issubset(valid_chars):
            invalid = set(cube_state) - valid_chars
            return False, f"Invalid characters: {invalid}"
        
        # Check that each color appears exactly 9 times
        color_counts = {}
        for char in cube_state:
            color_counts[char] = color_counts.get(char, 0) + 1
        
        for color in valid_chars:
            if color_counts.get(color, 0) != 9:
                return False, f"Color {color} appears {color_counts.get(color, 0)} times, should be 9"
        
        # Check center pieces (they define the face colors)
        centers = {
            'U': cube_state[4],   # Up center
            'R': cube_state[13],  # Right center
            'F': cube_state[22],  # Front center
            'D': cube_state[31],  # Down center
            'L': cube_state[40],  # Left center
            'B': cube_state[49]   # Back center
        }
        
        # Each center should match its expected color
        for face, center_color in centers.items():
            if center_color != face:
                return False, f"Center of {face} face should be {face}, got {center_color}"
        
        return True, "Valid"
        
    except Exception as e:
        return False, f"Validation error: {e}"

def get_move_count(solution: str) -> int:
    """
    Count the number of moves in a solution string
    
    Args:
        solution: Solution string with space-separated moves
        
    Returns:
        Number of moves
    """
    if not solution or not solution.strip():
        return 0
    return len(solution.strip().split())

def optimize_solution(solution: str) -> str:
    """
    Basic optimization of move sequences (remove redundant moves)
    
    Args:
        solution: Original solution string
        
    Returns:
        Optimized solution string
    """
    if not solution:
        return solution
    
    moves = solution.split()
    optimized = []
    
    i = 0
    while i < len(moves):
        current_move = moves[i]
        
        # Look ahead for consecutive same moves
        same_moves = [current_move]
        j = i + 1
        
        base_move = current_move.rstrip("'2")
        while j < len(moves) and moves[j].rstrip("'2") == base_move:
            same_moves.append(moves[j])
            j += 1
        
        # Combine same moves
        if len(same_moves) > 1:
            total_rotation = sum_rotations(same_moves)
            if total_rotation:
                optimized.append(total_rotation)
        else:
            optimized.append(current_move)
        
        i = j
    
    return " ".join(optimized)

def sum_rotations(moves: list) -> Optional[str]:
    """
    Sum up rotations of the same face
    
    Args:
        moves: List of moves of the same face
        
    Returns:
        Combined move or None if they cancel out
    """
    if not moves:
        return None
    
    base_move = moves[0].rstrip("'2")
    total = 0
    
    for move in moves:
        if move == base_move:
            total += 1
        elif move == base_move + "'":
            total -= 1
        elif move == base_move + "2":
            total += 2
    
    # Normalize to 0-3 range
    total = total % 4
    
    if total == 0:
        return None
    elif total == 1:
        return base_move
    elif total == 2:
        return base_move + "2"
    elif total == 3:
        return base_move + "'"

# Example usage and testing
if __name__ == "__main__":
    # Test with a scrambled cube state
    test_state = "DRLUUBFBRBLURRLRUBLRDDFDFFLUUFFDUDFDRRRUUUDLLLLBDBFBBB"
    
    try:
        print(f"Testing solver with state: {test_state}")
        solution = solve_cube(test_state)
        print(f"Solution: {solution}")
        print(f"Move count: {get_move_count(solution)}")
        
        # Test optimization
        optimized = optimize_solution(solution)
        print(f"Optimized: {optimized}")
        print(f"Optimized move count: {get_move_count(optimized)}")
        
    except SolverError as e:
        print(f"Solver error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")