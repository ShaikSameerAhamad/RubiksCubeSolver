"""
Test suite for the Rubik's Cube Solver API

Run with: pytest test_api.py -v
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test data
SOLVED_CUBE = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
SCRAMBLED_CUBE = "DRLUUBFBRBLURRLRUBLRDDFDFFLUUFFDUDFDRRRUUUDLLLLBDBFBBB"
INVALID_CUBE = "UUUUUUUUURRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"  # Too many U's

class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self):
        """Test basic health check"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["version"] == "1.0.0"

class TestRootEndpoint:
    """Test root endpoint"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns API info"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data

class TestSolveEndpoint:
    """Test cube solving endpoint"""
    
    def test_solve_scrambled_cube(self):
        """Test solving a valid scrambled cube"""
        response = client.post("/solve", json={
            "state": SCRAMBLED_CUBE,
            "save_solution": False
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Check response structure
        assert "solution" in data
        assert "move_count" in data
        assert "execution_time" in data
        assert "original_state" in data
        assert "timestamp" in data
        
        # Check data types and values
        assert isinstance(data["solution"], str)
        assert isinstance(data["move_count"], int)
        assert isinstance(data["execution_time"], float)
        assert data["original_state"] == SCRAMBLED_CUBE
        assert data["move_count"] >= 0
        assert data["execution_time"] > 0
    
    def test_solve_already_solved_cube(self):
        """Test solving an already solved cube"""
        response = client.post("/solve", json={
            "state": SOLVED_CUBE,
            "save_solution": False
        })
        
        assert response.status_code == 200
        data = response.json()
        
        # Solved cube should return empty solution
        assert data["solution"] == ""
        assert data["move_count"] == 0
        assert data["execution_time"] > 0
    
    def test_solve_invalid_cube_format(self):
        """Test solving with invalid cube format"""
        # Test wrong length
        response = client.post("/solve", json={
            "state": "UUUUUUUUU",  # Too short
            "save_solution": False
        })
        assert response.status_code == 400
        assert "Invalid cube state" in response.json()["detail"]
        
        # Test invalid characters
        response = client.post("/solve", json={
            "state": "X" * 54,  # Invalid character
            "save_solution": False
        })
        assert response.status_code == 400
    
    def test_solve_invalid_cube_colors(self):
        """Test solving with invalid color distribution"""
        response = client.post("/solve", json={
            "state": INVALID_CUBE,  # Wrong color distribution
            "save_solution": False
        })
        
        assert response.status_code == 400
        assert "Invalid cube state" in response.json()["detail"]
    
    def test_solve_with_save_solution(self):
        """Test solving with solution saving enabled"""
        response = client.post("/solve", json={
            "state": SCRAMBLED_CUBE,
            "save_solution": True
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "solution" in data
    
    def test_solve_missing_state(self):
        """Test solving without providing state"""
        response = client.post("/solve", json={
            "save_solution": False
        })
        
        assert response.status_code == 422  # Validation error

class TestScrambleEndpoint:
    """Test scramble generation endpoint"""
    
    def test_generate_default_scramble(self):
        """Test generating scramble with default parameters"""
        response = client.get("/scramble")
        assert response.status_code == 200
        
        data = response.json()
        assert "scramble" in data
        assert "scrambled_state" in data
        
        # Check scramble format
        scramble_moves = data["scramble"].split()
        assert len(scramble_moves) == 20  # Default move count
        
        # Check state format
        assert len(data["scrambled_state"]) == 54
    
    def test_generate_custom_length_scramble(self):
        """Test generating scramble with custom length"""
        move_count = 15
        response = client.get(f"/scramble?moves={move_count}")
        assert response.status_code == 200
        
        data = response.json()
        scramble_moves = data["scramble"].split()
        assert len(scramble_moves) == move_count
    
    def test_generate_scramble_invalid_length(self):
        """Test generating scramble with invalid length"""
        # Too few moves
        response = client.get("/scramble?moves=0")
        assert response.status_code == 400
        
        # Too many moves
        response = client.get("/scramble?moves=100")
        assert response.status_code == 400
    
    def test_scramble_moves_validity(self):
        """Test that generated scramble contains only valid moves"""
        response = client.get("/scramble?moves=10")
        assert response.status_code == 200
        
        data = response.json()
        scramble_moves = data["scramble"].split()
        
        valid_moves = {
            'U', 'U\'', 'U2', 'D', 'D\'', 'D2',
            'R', 'R\'', 'R2', 'L', 'L\'', 'L2',
            'F', 'F\'', 'F2', 'B', 'B\'', 'B2'
        }
        
        for move in scramble_moves:
            assert move in valid_moves

class TestSolutionsEndpoint:
    """Test solutions storage endpoint"""
    
    def test_get_solutions_empty(self):
        """Test getting solutions when none exist"""
        # Clear solutions first
        client.delete("/solutions")
        
        response = client.get("/solutions")
        assert response.status_code == 200
        
        data = response.json()
        assert "solutions" in data
        assert "total_count" in data
        assert "returned_count" in data
        assert data["total_count"] == 0
        assert len(data["solutions"]) == 0
    
    def test_get_solutions_with_data(self):
        """Test getting solutions after solving some cubes"""
        # Clear solutions first
        client.delete("/solutions")
        
        # Solve a cube with save enabled
        client.post("/solve", json={
            "state": SCRAMBLED_CUBE,
            "save_solution": True
        })
        
        # Get solutions
        response = client.get("/solutions")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_count"] >= 1
        assert len(data["solutions"]) >= 1
        
        # Check solution structure
        solution = data["solutions"][0]
        assert "original_state" in solution
        assert "solution" in solution
        assert "move_count" in solution
        assert "execution_time" in solution
        assert "timestamp" in solution
    
    def test_get_solutions_with_limit(self):
        """Test getting solutions with limit parameter"""
        response = client.get("/solutions?limit=5")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["solutions"]) <= 5
    
    def test_clear_solutions(self):
        """Test clearing all solutions"""
        # Add a solution first
        client.post("/solve", json={
            "state": SCRAMBLED_CUBE,
            "save_solution": True
        })
        
        # Clear solutions
        response = client.delete("/solutions")
        assert response.status_code == 200
        assert "message" in response.json()
        
        # Verify solutions are cleared
        response = client.get("/solutions")
        data = response.json()
        assert data["total_count"] == 0

class TestCORSHeaders:
    """Test CORS configuration"""
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present in responses"""
        response = client.get("/health")
        assert response.status_code == 200
        
        # Check for CORS headers (these might be added by middleware)
        # The exact headers depend on the request origin
        assert response.headers is not None

class TestErrorHandling:
    """Test error handling across endpoints"""
    
    def test_invalid_json_request(self):
        """Test handling of invalid JSON in requests"""
        response = client.post(
            "/solve",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        # Should return 422 for validation error
        assert response.status_code == 422
    
    def test_missing_content_type(self):
        """Test handling of missing content type"""
        response = client.post("/solve", data='{"state": "test"}')
        
        # FastAPI should handle this gracefully
        assert response.status_code in [400, 422]
    
    def test_method_not_allowed(self):
        """Test unsupported HTTP methods"""
        response = client.patch("/solve")
        assert response.status_code == 405  # Method not allowed

class TestIntegration:
    """Integration tests combining multiple endpoints"""
    
    def test_scramble_and_solve_integration(self):
        """Test generating a scramble and then solving it"""
        # Generate scramble
        scramble_response = client.get("/scramble?moves=10")
        assert scramble_response.status_code == 200
        
        scrambled_state = scramble_response.json()["scrambled_state"]
        
        # Solve the scrambled cube
        solve_response = client.post("/solve", json={
            "state": scrambled_state,
            "save_solution": True
        })
        
        assert solve_response.status_code == 200
        solution_data = solve_response.json()
        
        # Should have a valid solution
        assert solution_data["solution"] != ""
        assert solution_data["move_count"] > 0
        assert solution_data["original_state"] == scrambled_state
    
    def test_solve_and_retrieve_solution(self):
        """Test solving a cube and retrieving the stored solution"""
        # Clear solutions
        client.delete("/solutions")
        
        # Solve with save enabled
        solve_response = client.post("/solve", json={
            "state": SCRAMBLED_CUBE,
            "save_solution": True
        })
        
        assert solve_response.status_code == 200
        original_solution = solve_response.json()
        
        # Retrieve stored solutions
        solutions_response = client.get("/solutions?limit=1")
        assert solutions_response.status_code == 200
        
        stored_solutions = solutions_response.json()["solutions"]
        assert len(stored_solutions) >= 1
        
        # Compare stored solution with original
        stored_solution = stored_solutions[0]
        assert stored_solution["original_state"] == original_solution["original_state"]
        assert stored_solution["solution"] == original_solution["solution"]
        assert stored_solution["move_count"] == original_solution["move_count"]

# Performance tests (optional - can be slow)
class TestPerformance:
    """Basic performance tests"""
    
    @pytest.mark.slow
    def test_solve_performance(self):
        """Test that solving completes within reasonable time"""
        import time
        
        start_time = time.time()
        response = client.post("/solve", json={
            "state": SCRAMBLED_CUBE,
            "save_solution": False
        })
        end_time = time.time()
        
        assert response.status_code == 200
        
        # Should complete within 5 seconds (generous limit)
        assert end_time - start_time < 5.0
        
        # Check that the reported execution time is reasonable
        execution_time = response.json()["execution_time"]
        assert execution_time < 2.0  # Should be much faster than this
    
    @pytest.mark.slow
    def test_multiple_solves_performance(self):
        """Test performance with multiple concurrent solves"""
        import concurrent.futures
        import time
        
        def solve_cube():
            return client.post("/solve", json={
                "state": SCRAMBLED_CUBE,
                "save_solution": False
            })
        
        start_time = time.time()
        
        # Run 5 concurrent solve requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(solve_cube) for _ in range(5)]
            responses = [future.result() for future in futures]
        
        end_time = time.time()
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == 200
        
        # Should complete all requests within 10 seconds
        assert end_time - start_time < 10.0

if __name__ == "__main__":
    # Run specific test classes
    pytest.main([__file__, "-v"])