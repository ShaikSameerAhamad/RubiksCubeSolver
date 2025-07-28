# Rubik's Cube Solver Backend

A FastAPI-based backend for solving Rubik's Cubes using Kociemba's Two-Phase Algorithm.

## 🚀 Features

- **Fast Solving**: Uses the optimized `kociemba` library for quick cube solving
- **Comprehensive Validation**: Validates cube states for physical possibility
- **RESTful API**: Clean FastAPI endpoints with automatic documentation
- **Multiple Formats**: Supports various input/output formats
- **Scramble Generation**: Built-in random scramble generator
- **Solution Storage**: Optional saving of solutions to disk
- **Performance Tracking**: Execution time and move count analytics

## 📋 Requirements

- Python 3.8+
- pip or conda package manager

## 🛠 Installation

1. **Clone or create the project directory:**
```bash
mkdir rubik-backend
cd rubik-backend
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## 🏃 Running the Server

### Development Mode
```bash
python main.py
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **Main API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 API Endpoints

### `POST /solve`
Solve a scrambled Rubik's cube.

**Request:**
```json
{
  "state": "DRLUUBFBRBLURRLRUBLRDDFDFFLUUFFDUDFDRRRUUUDLLLLBDBFBBB",
  "save_solution": false
}
```

**Response:**
```json
{
  "solution": "U R2 F R' B L U2 B2 D2 R'",
  "move_count": 10,
  "execution_time": 0.0234,
  "original_state": "DRLUUBFBRBLURRLRUBLRDDFD...",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

### `GET /scramble`
Generate a random scramble sequence.

**Query Parameters:**
- `moves` (optional): Number of moves (1-50, default: 20)

**Response:**
```json
{
  "scramble": "R U R' U' R' F R2 U' R' U' R U R' F'",
  "scrambled_state": "DRLUUBFBRBLURRLRUBLRDDFDFFLUUFFDUDFDRRRUUUDLLLLBDBFBBB"
}
```

### `GET /health`
Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:45.123456",
  "version": "1.0.0"
}
```

### `GET /solutions`
Get recent solutions from storage.

**Query Parameters:**
- `limit` (optional): Maximum solutions to return (default: 10)

**Response:**
```json
{
  "solutions": [
    {
      "original_state": "DRLUUBFBR...",
      "solution": "U R2 F R' B L U2 B2 D2 R'",
      "move_count": 10,
      "execution_time": 0.0234,
      "timestamp": "2024-01-15T10:30:45.123456"
    }
  ],
  "total_count": 1,
  "returned_count": 1
}
```

## 🧩 Cube State Format

The API uses a 54-character string to represent cube states:

### Kociemba Format
- **Characters**: `U` (Up/White), `D` (Down/Yellow), `R` (Right/Red), `L` (Left/Orange), `F` (Front/Green), `B` (Back/Blue)
- **Layout**: Positions 0-53 represent facelets in this order:
  - 0-8: Up face (U)
  - 9-17: Right face (R)
  - 18-26: Front face (F)
  - 27-35: Down face (D)
  - 36-44: Left face (L)
  - 45-53: Back face (B)

### Example States

**Solved Cube:**
```
UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB
```

**Scrambled Cube:**
```
DRLUUBFBRBLURRLRUBLRDDFDFFLUUFFDUDFDRRRUUUDLLLLBDBFBBB
```

## 🎯 Move Notation

The solver supports standard Rubik's cube notation:

### Basic Moves
- `U`, `D`, `R`, `L`, `F`, `B` - Clockwise 90° rotations
- `U'`, `D'`, `R'`, `L'`, `F'`, `B'` - Counter-clockwise 90° rotations  
- `U2`, `D2`, `R2`, `L2`, `F2`, `B2` - 180° rotations

### Example Solution
```
U R2 D' F B' L2 U' B2 D2 R'
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file for configuration:

```bash
# API Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS Settings
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]

# Solver Settings
MAX_SOLVE_DEPTH=24
SOLVE_TIMEOUT=10

# Storage Settings
SOLUTIONS_FILE=solutions.json
MAX_STORED_SOLUTIONS=1000
```

## 🧪 Testing

### Manual Testing
Test the API using curl:

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test scramble generation
curl http://localhost:8000/scramble?moves=15

# Test cube solving
curl -X POST http://localhost:8000/solve \
  -H "Content-Type: application/json" \
  -d '{"state": "DRLUUBFBRBLURRLRUBLRDDFDFFLUUFFDUDFDRRRUUUDLLLLBDBFBBB"}'
```

### Automated Testing
Run the test suite:

```bash
pytest tests/ -v
```

### Test Cases
The backend includes validation for:
- ✅ Cube state format (54 characters, valid colors)
- ✅ Color distribution (9 of each color)
- ✅ Center piece positions
- ✅ Edge and corner piece validity
- ✅ Physical cube constraints

## 🏗 Architecture

### Project Structure
```
rubik-backend/
├── main.py              # FastAPI application
├── solver.py            # Kociemba solver implementation
├── validator.py         # Cube state validation
├── cube_utils.py        # Utility functions
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .env                # Environment configuration
├── solutions.json      # Stored solutions (created automatically)
└── tests/              # Test suite
    ├── test_solver.py
    ├── test_validator.py
    └── test_api.py
```

### Key Components

1. **FastAPI App** (`main.py`)
   - RESTful API endpoints
   - Request/response models
   - Error handling
   - CORS configuration

2. **Solver Engine** (`solver.py`)
   - Kociemba algorithm integration
   - Solution optimization
   - Performance tracking

3. **Validator** (`validator.py`)
   - Comprehensive cube state validation
   - Physical constraint checking
   - Error reporting

4. **Utilities** (`cube_utils.py`)
   - Format conversion
   - Move application
   - Scramble generation

## 🔗 Frontend Integration

### JavaScript/TypeScript Example
```javascript
// Solve a cube
async function solveCube(cubeState) {
  const response = await fetch('http://localhost:8000/solve', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      state: cubeState,
      save_solution: true
    })
  });
  
  const result = await response.json();
  return result.solution;
}

// Generate scramble
async function generateScramble(moves = 20) {
  const response = await fetch(`http://localhost:8000/scramble?moves=${moves}`);
  const result = await response.json();
  return result;
}
```

### React Hook Example
```typescript
import { useState } from 'react';

interface SolveResult {
  solution: string;
  move_count: number;
  execution_time: number;
}

export function useCubeSolver() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const solveCube = async (cubeState: string): Promise<SolveResult | null> => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/solve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ state: cubeState })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      return null;
    } finally {
      setLoading(false);
    }
  };

  return { solveCube, loading, error };
}
```

## 📊 Performance

### Typical Performance Metrics
- **Average solve time**: 20-100ms
- **Maximum moves**: Usually under 25 moves
- **Memory usage**: ~50MB baseline
- **Throughput**: 100+ solves/second

### Optimization Tips
1. Keep the server running (avoid cold starts)
2. Use connection pooling for multiple requests
3. Cache scrambled states for testing
4. Monitor memory usage with many stored solutions

## 🚨 Error Handling

### Common Error Responses

**Invalid Cube State (400):**
```json
{
  "detail": "Invalid cube state: Color U appears 10 times (should be 9)"
}
```

**Unsolvable Cube (400):**
```json
{
  "detail": "Invalid or unsolvable cube state: Invalid edge piece color combinations"
}
```

**Server Error (500):**
```json
{
  "detail": "Error solving cube: Solver timed out after 10 seconds"
}
```

## 🛡 Security Considerations

- Input validation prevents malformed requests
- No persistent storage of sensitive data
- Rate limiting recommended for production
- CORS configured for specific origins

## 🚀 Deployment

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations
- Use a process manager like Gunicorn
- Configure proper logging
- Set up health checks
- Use environment variables for secrets
- Consider Redis for solution caching

## 📄 License

This project is open source. See LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📞 Support

For issues and questions:
- Check the `/docs` endpoint for API documentation
- Review validation error messages
- Test with the provided examples
- Check server logs for detailed error information