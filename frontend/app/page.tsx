"use client"

import { useState } from "react"
import { CubeInterface } from "@/components/cube-interface"
import { MoveDisplay } from "@/components/move-display"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Loader2, RotateCcw, Zap } from "lucide-react"
// CORRECTED IMPORT: Added getScramble
import { solveCube, scrambleCube } from "@/lib/api"
import { generateScrambledState } from "@/lib/cube-utils"

export default function RubiksCubeSolver() {
  const SOLVED_STATE = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
  const [cubeState, setCubeState] = useState<string>(SOLVED_STATE)
  const [moves, setMoves] = useState<string[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [solveTime, setSolveTime] = useState<number | null>(null)

  // Check if cube is in solved state
  const isSolved = (state: string) => state === SOLVED_STATE

  // Check if cube is scrambled (not solved)
  const isScrambled = !isSolved(cubeState);

  // Handle manual cube state changes
  const handleCubeStateChange = (newState: string) => {
    if (isLoading) return;
    setCubeState(newState)
    setMoves([])
    setError(null)
    setSolveTime(null)
  }

  const handleScramble = async () => {
    if (isLoading) return;
    setIsLoading(true);
    setError(null);
    setMoves([]);
    setSolveTime(null);
    try {
      // Use getScramble from API
      const response = await scrambleCube();
      if (!response || !response.success || !response.data || !response.data.state) {
        throw new Error("Invalid response from server");
      }
      setCubeState(response.data.state);
    } catch (error) {
      setError(error instanceof Error ? error.message : "Failed to fetch scramble from API.");
    }
    setIsLoading(false);
  }

  const handleSolve = async () => {
    if (isLoading || isSolved(cubeState)) return;
    setIsLoading(true);
    setError(null);
    setSolveTime(null);
    try {
      const startTime = Date.now();
      const result = await solveCube(cubeState);
      const endTime = Date.now();
      if (!result || !result.success || !result.data) {
        throw new Error("Invalid response from server");
      }
      const solution = result.data.solution || "";
      setMoves(solution ? solution.split(' ') : []);
      setSolveTime(endTime - startTime);
    } catch (error) {
      setError(error instanceof Error ? error.message : "Failed to solve cube");
    } finally {
      setIsLoading(false);
    }
  }

  const handleReset = () => {
    if (isLoading) return;
    setCubeState(SOLVED_STATE);
    setMoves([]);
    setError(null);
    setSolveTime(null);
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Rubik's Cube Solver</h1>
          <p className="text-lg text-gray-600">
            Configure your cube state and get the optimal solution using Kociemba's Two-Phase Algorithm
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Cube Interface */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <div className="w-6 h-6 bg-gradient-to-r from-red-500 to-orange-500 rounded"></div>
                Cube Configuration
              </CardTitle>
              <CardDescription>
                Click on each sticker to change its color. Configure all 6 faces of the cube.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <CubeInterface cubeState={cubeState} onStateChange={handleCubeStateChange} />

              <div className="flex gap-2 mt-6">
              <Button onClick={handleScramble} variant="outline" className="flex-1 bg-transparent" disabled={isLoading}>
                <RotateCcw className="w-4 h-4 mr-2" />
                Scramble
              </Button>
              <Button onClick={handleReset} variant="outline" className="flex-1 bg-transparent" disabled={isLoading || isSolved(cubeState)}>
                Reset
              </Button>
              </div>
            </CardContent>
          </Card>

          {/* Solution Display */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Zap className="w-5 h-5 text-yellow-500" />
                Solution
              </CardTitle>
              <CardDescription>
                Click solve to get the optimal move sequence for your cube configuration.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button 
                onClick={handleSolve} 
                disabled={isLoading || isSolved(cubeState)} 
                className="w-full mb-4" 
                size="lg"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Solving...
                  </>
                ) : (
                  <>
                    <Zap className="w-4 h-4 mr-2" />
                    Solve Cube
                  </>
                )}
              </Button>

              {!isScrambled && !isLoading && (
                <div className="mb-4 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-700 rounded-lg">
                  <p className="text-sm text-blue-700 dark:text-blue-300">💡 Click "Scramble" to generate a scrambled cube, then you can solve it!</p>
                </div>
              )}

              {error && (
                <Alert variant="destructive" className="mb-4">
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              {solveTime !== null && moves.length > 0 && !error && (
                <div className="mb-4 p-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-700 rounded-lg">
                  <p className="text-sm text-green-700 dark:text-green-300">✅ Solved in {solveTime}ms with {moves.length} moves.</p>
                </div>
              )}
              
              {solveTime !== null && moves.length === 0 && !error && (
                 <div className="mb-4 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-700 rounded-lg">
                  <p className="text-sm text-blue-700 dark:text-blue-300">Cube is already solved!</p>
                </div>
              )}

              <MoveDisplay moves={moves} />
            </CardContent>
          </Card>
        </div>

        {/* API Status */}
        <Card className="mt-8">
          <CardContent className="pt-6">
            <div className="text-center text-sm text-gray-500">
              <p>Backend API: {process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"}</p>
              <p className="mt-1">Make sure your FastAPI backend is running and accessible at the configured URL.</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
