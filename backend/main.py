from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import time
import json
import os
from datetime import datetime
from typing import Optional, List, Dict

from solver import solve_cube
from validator import validate_cube_state, CubeValidationError
from cube_utils import convert_to_kociemba_format, generate_scramble

app = FastAPI(
    title="Rubik's Cube Solver API",
    description="A FastAPI backend for solving Rubik's Cubes using Kociemba's Two-Phase Algorithm",
    version="1.0.0"
)

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Next.js default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class CubeState(BaseModel):
    state: str = Field(..., description="54-character cube state string using UDLRFB notation")
    save_solution: Optional[bool] = Field(default=False, description="Whether to save the solution to disk")

class SolveResponse(BaseModel):
    solution: str = Field(..., description="Solution move sequence")
    move_count: int = Field(..., description="Number of moves in solution")
    execution_time: float = Field(..., description="Time taken to solve in seconds")
    original_state: str = Field(..., description="Original cube state")
    timestamp: str = Field(..., description="When the solution was generated")

class ScrambleResponse(BaseModel):
    scramble: str = Field(..., description="Random scramble sequence")
    scrambled_state: str = Field(..., description="Resulting cube state after scramble")

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str

# Storage for solutions (in production, use a proper database)
SOLUTIONS_FILE = "solutions.json"

def load_solutions() -> List[Dict]:
    """Load solutions from JSON file"""
    if os.path.exists(SOLUTIONS_FILE):
        try:
            with open(SOLUTIONS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_solution_to_file(solution_data: Dict):
    """Save solution to JSON file"""
    solutions = load_solutions()
    solutions.append(solution_data)
    
    # Keep only last 1000 solutions to prevent file from growing too large
    if len(solutions) > 1000:
        solutions = solutions[-1000:]
    
    try:
        with open(SOLUTIONS_FILE, 'w') as f:
            json.dump(solutions, f, indent=2)
    except IOError as e:
        print(f"Warning: Could not save solution to file: {e}")

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Rubik's Cube Solver API",
        "version": "1.0.0",
        "endpoints": {
            "solve": "POST /solve - Solve a Rubik's cube",
            "scramble": "GET /scramble - Generate a random scramble",
            "health": "GET /health - Check API health",
            "solutions": "GET /solutions - Get recent solutions"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )

@app.post("/solve", response_model=SolveResponse)
async def solve_cube_endpoint(cube_state: CubeState):
    """
    Solve a Rubik's cube from the given state
    
    Args:
        cube_state: 54-character string representing the cube state
                   using UDLRFB notation (U=Up/White, D=Down/Yellow, etc.)
    
    Returns:
        Solution move sequence and metadata
    """
    try:
        start_time = time.time()
        
        # Validate the cube state
        validate_cube_state(cube_state.state)
        
        # Convert to Kociemba format if needed
        kociemba_state = convert_to_kociemba_format(cube_state.state)
        
        # Solve the cube
        solution = solve_cube(kociemba_state)
        
        execution_time = time.time() - start_time
        move_count = len(solution.split()) if solution else 0
        timestamp = datetime.now().isoformat()
        
        # Prepare response
        response = SolveResponse(
            solution=solution,
            move_count=move_count,
            execution_time=round(execution_time, 4),
            original_state=cube_state.state,
            timestamp=timestamp
        )
        
        # Save solution if requested
        if cube_state.save_solution:
            solution_data = {
                "original_state": cube_state.state,
                "solution": solution,
                "move_count": move_count,
                "execution_time": execution_time,
                "timestamp": timestamp
            }
            save_solution_to_file(solution_data)
        
        return response
        
    except CubeValidationError as e:
        raise HTTPException(status_code=400, detail=f"Invalid cube state: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error solving cube: {str(e)}")

@app.get("/scramble", response_model=ScrambleResponse)
async def generate_scramble_endpoint(moves: Optional[int] = 20):
    """
    Generate a random scramble sequence
    
    Args:
        moves: Number of moves in the scramble (default: 20)
    
    Returns:
        Random scramble sequence and resulting cube state
    """
    try:
        if moves < 1 or moves > 50:
            raise HTTPException(status_code=400, detail="Number of moves must be between 1 and 50")
        
        scramble, scrambled_state = generate_scramble(moves)
        
        return ScrambleResponse(
            scramble=scramble,
            scrambled_state=scrambled_state
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating scramble: {str(e)}")

@app.get("/solutions")
async def get_recent_solutions(limit: Optional[int] = 10):
    """
    Get recent solutions from storage
    
    Args:
        limit: Maximum number of solutions to return (default: 10)
    
    Returns:
        List of recent solutions
    """
    try:
        solutions = load_solutions()
        
        # Return most recent solutions first
        recent_solutions = solutions[-limit:] if solutions else []
        recent_solutions.reverse()
        
        return {
            "solutions": recent_solutions,
            "total_count": len(solutions),
            "returned_count": len(recent_solutions)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving solutions: {str(e)}")

@app.delete("/solutions")
async def clear_solutions():
    """Clear all stored solutions"""
    try:
        if os.path.exists(SOLUTIONS_FILE):
            os.remove(SOLUTIONS_FILE)
        
        return {"message": "Solutions cleared successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing solutions: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)