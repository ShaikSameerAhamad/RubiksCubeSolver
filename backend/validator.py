"""
Cube State Validator

This module provides comprehensive validation for Rubik's cube states,
ensuring they are physically possible and properly formatted.
"""

from typing import Dict, List, Set, Tuple
import re

class CubeValidationError(Exception):
    """Custom exception for cube validation errors"""
    pass

# Standard color mappings for cube faces
FACE_COLORS = {
    'U': 'White',    # Up face - traditionally white
    'D': 'Yellow',   # Down face - traditionally yellow  
    'R': 'Red',      # Right face - traditionally red
    'L': 'Orange',   # Left face - traditionally orange
    'F': 'Green',    # Front face - traditionally green
    'B': 'Blue'      # Back face - traditionally blue
}

# Face indices in the 54-character string
FACE_INDICES = {
    'U': list(range(0, 9)),     # Up face: 0-8
    'R': list(range(9, 18)),    # Right face: 9-17
    'F': list(range(18, 27)),   # Front face: 18-26
    'D': list(range(27, 36)),   # Down face: 27-35
    'L': list(range(36, 45)),   # Left face: 36-44
    'B': list(range(45, 54))    # Back face: 45-53
}

# Center piece positions (these define the face colors)
CENTER_POSITIONS = {
    'U': 4,   # Up center
    'R': 13,  # Right center
    'F': 22,  # Front center
    'D': 31,  # Down center
    'L': 40,  # Left center
    'B': 49   # Back center
}

# Edge and corner piece positions for advanced validation
EDGE_POSITIONS = [
    (1, 46), (3, 37), (5, 10), (7, 19),     # Up face edges
    (12, 23), (14, 32), (16, 48), (25, 41), # Middle layer edges
    (28, 50), (30, 39), (34, 16), (52, 43)  # Down face edges
]

CORNER_POSITIONS = [
    (0, 36, 47), (2, 9, 45), (6, 18, 38), (8, 20, 11),    # Up face corners
    (24, 15, 33), (26, 17, 29), (35, 51, 42), (53, 44, 27) # Down face corners
]

def validate_cube_state(cube_state: str) -> None:
    """
    Comprehensive validation of a cube state
    
    Args:
        cube_state: 54-character string representing the cube state
        
    Raises:
        CubeValidationError: If the cube state is invalid
    """
    try:
        # Basic format validation
        _validate_format(cube_state)
        
        # Color count validation
        _validate_color_distribution(cube_state)
        
        # Center piece validation
        _validate_centers(cube_state)
        
        # Advanced geometric validation
        _validate_cube_geometry(cube_state)
        
    except CubeValidationError:
        raise
    except Exception as e:
        raise CubeValidationError(f"Validation failed: {e}")

def _validate_format(cube_state: str) -> None:
    """Validate basic format requirements"""
    
    # Check length
    if len(cube_state) != 54:
        raise CubeValidationError(
            f"Cube state must be exactly 54 characters long, got {len(cube_state)}"
        )
    
    # Check valid characters
    valid_chars = set('UDLRFB')
    cube_chars = set(cube_state)
    invalid_chars = cube_chars - valid_chars
    
    if invalid_chars:
        raise CubeValidationError(
            f"Invalid characters found: {sorted(invalid_chars)}. "
            f"Only U, D, L, R, F, B are allowed."
        )
    
    # Check that all required colors are present
    missing_colors = valid_chars - cube_chars
    if missing_colors:
        raise CubeValidationError(
            f"Missing required colors: {sorted(missing_colors)}"
        )

def _validate_color_distribution(cube_state: str) -> None:
    """Validate that each color appears exactly 9 times"""
    
    color_counts = {}
    for char in cube_state:
        color_counts[char] = color_counts.get(char, 0) + 1
    
    errors = []
    for color in 'UDLRFB':
        count = color_counts.get(color, 0)
        if count != 9:
            color_name = FACE_COLORS[color]
            errors.append(f"{color} ({color_name}): {count} (should be 9)")
    
    if errors:
        raise CubeValidationError(
            f"Invalid color distribution:\n" + "\n".join(errors)
        )

def _validate_centers(cube_state: str) -> None:
    """Validate that center pieces are in correct positions"""
    
    errors = []
    for face, center_pos in CENTER_POSITIONS.items():
        center_color = cube_state[center_pos]
        if center_color != face:
            expected_color = FACE_COLORS[face]
            actual_color = FACE_COLORS[center_color]
            errors.append(
                f"{face} face center should be {face} ({expected_color}), "
                f"got {center_color} ({actual_color})"
            )
    
    if errors:
        raise CubeValidationError(
            "Invalid center pieces:\n" + "\n".join(errors)
        )

def _validate_cube_geometry(cube_state: str) -> None:
    """
    Advanced validation to check if the cube state is geometrically possible
    This includes edge and corner piece validation
    """
    
    # Validate edge pieces
    _validate_edge_pieces(cube_state)
    
    # Validate corner pieces  
    _validate_corner_pieces(cube_state)
    
    # Check overall cube parity
    _validate_cube_parity(cube_state)

def _validate_edge_pieces(cube_state: str) -> None:
    """Validate that edge pieces have valid color combinations"""
    
    # Define valid edge piece color combinations
    valid_edges = {
        frozenset(['U', 'F']), frozenset(['U', 'R']), frozenset(['U', 'B']), frozenset(['U', 'L']),
        frozenset(['D', 'F']), frozenset(['D', 'R']), frozenset(['D', 'B']), frozenset(['D', 'L']),
        frozenset(['F', 'R']), frozenset(['F', 'L']), frozenset(['B', 'R']), frozenset(['B', 'L'])
    }
    
    found_edges = []
    invalid_edges = []
    
    for pos1, pos2 in EDGE_POSITIONS:
        if pos1 < len(cube_state) and pos2 < len(cube_state):
            edge_colors = frozenset([cube_state[pos1], cube_state[pos2]])
            found_edges.append(edge_colors)
            
            if edge_colors not in valid_edges:
                invalid_edges.append((pos1, pos2, edge_colors))
    
    if invalid_edges:
        error_details = []
        for pos1, pos2, colors in invalid_edges:
            color_names = [FACE_COLORS[c] for c in colors]
            error_details.append(f"Positions {pos1},{pos2}: {list(colors)} ({color_names})")
        
        raise CubeValidationError(
            f"Invalid edge piece color combinations:\n" + "\n".join(error_details)
        )
    
    # Check that each valid edge appears exactly once
    edge_counts = {}
    for edge in found_edges:
        edge_counts[edge] = edge_counts.get(edge, 0) + 1
    
    duplicate_edges = [edge for edge, count in edge_counts.items() if count > 1]
    missing_edges = valid_edges - set(found_edges)
    
    if duplicate_edges or missing_edges:
        errors = []
        if duplicate_edges:
            errors.append(f"Duplicate edges: {duplicate_edges}")
        if missing_edges:
            errors.append(f"Missing edges: {missing_edges}")
        
        raise CubeValidationError("Edge piece distribution error:\n" + "\n".join(errors))

def _validate_corner_pieces(cube_state: str) -> None:
    """Validate that corner pieces have valid color combinations"""
    
    # Define valid corner piece color combinations
    valid_corners = {
        frozenset(['U', 'F', 'R']), frozenset(['U', 'R', 'B']),
        frozenset(['U', 'B', 'L']), frozenset(['U', 'L', 'F']),
        frozenset(['D', 'F', 'L']), frozenset(['D', 'L', 'B']),
        frozenset(['D', 'B', 'R']), frozenset(['D', 'R', 'F'])
    }
    
    found_corners = []
    invalid_corners = []
    
    for pos1, pos2, pos3 in CORNER_POSITIONS:
        if all(pos < len(cube_state) for pos in [pos1, pos2, pos3]):
            corner_colors = frozenset([cube_state[pos1], cube_state[pos2], cube_state[pos3]])
            found_corners.append(corner_colors)
            
            if corner_colors not in valid_corners:
                invalid_corners.append((pos1, pos2, pos3, corner_colors))
    
    if invalid_corners:
        error_details = []
        for pos1, pos2, pos3, colors in invalid_corners:
            color_names = [FACE_COLORS[c] for c in colors]
            error_details.append(f"Positions {pos1},{pos2},{pos3}: {list(colors)} ({color_names})")
        
        raise CubeValidationError(
            f"Invalid corner piece color combinations:\n" + "\n".join(error_details)
        )
    
    # Check that each valid corner appears exactly once
    corner_counts = {}
    for corner in found_corners:
        corner_counts[corner] = corner_counts.get(corner, 0) + 1
    
    duplicate_corners = [corner for corner, count in corner_counts.items() if count > 1]
    missing_corners = valid_corners - set(found_corners)
    
    if duplicate_corners or missing_corners:
        errors = []
        if duplicate_corners:
            errors.append(f"Duplicate corners: {duplicate_corners}")
        if missing_corners:
            errors.append(f"Missing corners: {missing_corners}")
        
        raise CubeValidationError("Corner piece distribution error:\n" + "\n".join(errors))

def _validate_cube_parity(cube_state: str) -> None:
    """
    Validate cube parity (advanced geometric constraint)
    This is a simplified check - full parity validation is quite complex
    """
    
    # For now, we'll do a basic check that the cube isn't in an impossible state
    # A more complete implementation would check:
    # - Edge orientation parity
    # - Corner orientation parity  
    # - Edge/corner permutation parity
    
    # Simple check: if we have valid edges and corners, the basic structure is OK
    # More advanced parity checks would require implementing cube move simulation
    pass

def is_solved_state(cube_state: str) -> bool:
    """
    Check if the cube state represents a solved cube
    
    Args:
        cube_state: 54-character cube state string
        
    Returns:
        True if solved, False otherwise
    """
    try:
        validate_cube_state(cube_state)
        
        # Check if each face has uniform color
        for face, indices in FACE_INDICES.items():
            face_colors = [cube_state[i] for i in indices]
            if len(set(face_colors)) != 1:
                return False
            # The uniform color should match the face identifier
            if face_colors[0] != face:
                return False
                
        return True
        
    except CubeValidationError:
        return False

def get_validation_summary(cube_state: str) -> Dict[str, any]:
    """
    Get a detailed validation summary for a cube state
    
    Args:
        cube_state: 54-character cube state string
        
    Returns:
        Dictionary with validation results and details
    """
    summary = {
        'valid': False,
        'errors': [],
        'warnings': [],
        'details': {
            'length': len(cube_state),
            'color_counts': {},
            'centers_correct': False,
            'is_solved': False
        }
    }
    
    try:
        # Basic format check
        if len(cube_state) != 54:
            summary['errors'].append(f"Invalid length: {len(cube_state)} (should be 54)")
            return summary
        
        # Count colors
        for char in cube_state:
            summary['details']['color_counts'][char] = summary['details']['color_counts'].get(char, 0) + 1
        
        # Check character validity
        valid_chars = set('UDLRFB')
        invalid_chars = set(cube_state) - valid_chars
        if invalid_chars:
            summary['errors'].append(f"Invalid characters: {sorted(invalid_chars)}")
        
        # Check color distribution
        for color in 'UDLRFB':
            count = summary['details']['color_counts'].get(color, 0)
            if count != 9:
                summary['errors'].append(f"Color {color} appears {count} times (should be 9)")
        
        # Check centers
        centers_correct = True
        for face, center_pos in CENTER_POSITIONS.items():
            if cube_state[center_pos] != face:
                centers_correct = False
                summary['errors'].append(f"Center of {face} face is {cube_state[center_pos]} (should be {face})")
        
        summary['details']['centers_correct'] = centers_correct
        
        # If no errors so far, try full validation
        if not summary['errors']:
            try:
                validate_cube_state(cube_state)
                summary['valid'] = True
                summary['details']['is_solved'] = is_solved_state(cube_state)
            except CubeValidationError as e:
                summary['errors'].append(str(e))
        
    except Exception as e:
        summary['errors'].append(f"Validation failed: {e}")
    
    return summary

def create_solved_cube() -> str:
    """
    Create a solved cube state string
    
    Returns:
        54-character string representing a solved cube
    """
    return (
        "UUUUUUUUU" +  # Up face (white)
        "RRRRRRRRR" +  # Right face (red)
        "FFFFFFFFF" +  # Front face (green)
        "DDDDDDDDD" +  # Down face (yellow)
        "LLLLLLLLL" +  # Left face (orange)
        "BBBBBBBBB"    # Back face (blue)
    )

def normalize_cube_string(cube_input: str) -> str:
    """
    Normalize cube input string by removing whitespace and converting to uppercase
    
    Args:
        cube_input: Raw cube state input
        
    Returns:
        Normalized cube state string
    """
    # Remove all whitespace and convert to uppercase
    normalized = re.sub(r'\s+', '', cube_input.upper())
    
    # Handle common alternative notations
    replacements = {
        'W': 'U',  # White -> Up
        'Y': 'D',  # Yellow -> Down
        'G': 'F',  # Green -> Front (sometimes)
        'O': 'L'   # Orange -> Left (sometimes)
    }
    
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    
    return normalized

def get_face_string(cube_state: str, face: str) -> str:
    """
    Extract the color string for a specific face
    
    Args:
        cube_state: 54-character cube state
        face: Face identifier ('U', 'D', 'L', 'R', 'F', 'B')
        
    Returns:
        9-character string representing the face
    """
    if face not in FACE_INDICES:
        raise CubeValidationError(f"Invalid face: {face}")
    
    indices = FACE_INDICES[face]
    return ''.join(cube_state[i] for i in indices)

def format_cube_display(cube_state: str) -> str:
    """
    Format cube state for human-readable display
    
    Args:
        cube_state: 54-character cube state
        
    Returns:
        Multi-line string showing the cube layout
    """
    try:
        validate_cube_state(cube_state)
    except CubeValidationError as e:
        return f"Invalid cube state: {e}"
    
    # Extract faces
    faces = {}
    for face, indices in FACE_INDICES.items():
        face_colors = [cube_state[i] for i in indices]
        faces[face] = [face_colors[i:i+3] for i in range(0, 9, 3)]
    
    # Create display layout
    display_lines = []
    
    # Top face (U)
    for row in faces['U']:
        display_lines.append("    " + " ".join(row))
    
    # Middle row (L F R B)
    for i in range(3):
        line = " ".join(faces['L'][i]) + " " + " ".join(faces['F'][i]) + " " + \
               " ".join(faces['R'][i]) + " " + " ".join(faces['B'][i])
        display_lines.append(line)
    
    # Bottom face (D)
    for row in faces['D']:
        display_lines.append("    " + " ".join(row))
    
    return "\n".join(display_lines)

# Example usage and testing
if __name__ == "__main__":
    # Test with a solved cube
    solved_cube = create_solved_cube()
    print("Testing solved cube:")
    print(f"State: {solved_cube}")
    print(f"Valid: {get_validation_summary(solved_cube)['valid']}")
    print(f"Solved: {is_solved_state(solved_cube)}")
    print()
    
    # Test with an invalid cube
    invalid_cube = "UUUUUUUUURRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBX"
    print("Testing invalid cube:")
    summary = get_validation_summary(invalid_cube)
    print(f"Valid: {summary['valid']}")
    print(f"Errors: {summary['errors']}")
    print()
    
    # Test display formatting
    print("Cube display format:")
    print(format_cube_display(solved_cube))