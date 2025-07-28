"use client"

import { useState } from "react"
import { CubeInterface } from "@/components/cube-interface"
import { MoveDisplay } from "@/components/move-display"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Loader2, RotateCcw, Zap } from "lucide-react"
import { solveCube } from "@/lib/api"
import { generateScrambledState } from "@/lib/cube-utils"

export default function RubiksCubeSolver() {
  const [cubeState, setCubeState] = useState<string>("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB")
  const [moves, setMoves] = useState<string[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [solveTime, setSolveTime] = useState<number | null>(null)

  const handleScramble = () => {
    const scrambledState = generateScrambledState()
    setCubeState(scrambledState)
    setMoves([])
    setError(null)
    setSolveTime(null)
  }

  const handleSolve = async () => {
    setIsLoading(true)
    setError(null)
    setSolveTime(null)

    try {
      const startTime = Date.now()
      const result = await solveCube(cubeState)
      const endTime = Date.now()

      if (result.success) {
        setMoves(result.moves || [])
        setSolveTime(endTime - startTime)
      } else {
        setError(result.error || "Failed to solve cube")
      }
    } catch (err) {
      setError("Failed to connect to solver API. Make sure your backend is running.")
    } finally {
      setIsLoading(false)
    }
  }

  const handleReset = () => {
    setCubeState("UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB")
    setMoves([])
    setError(null)
    setSolveTime(null)
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
              <CubeInterface cubeState={cubeState} onStateChange={setCubeState} />

              <div className="flex gap-2 mt-6">
                <Button onClick={handleScramble} variant="outline" className="flex-1 bg-transparent">
                  <RotateCcw className="w-4 h-4 mr-2" />
                  Scramble
                </Button>
                <Button onClick={handleReset} variant="outline" className="flex-1 bg-transparent">
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
              <Button onClick={handleSolve} disabled={isLoading} className="w-full mb-4" size="lg">
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

              {error && (
                <Alert className="mb-4 border-red-200 bg-red-50">
                  <AlertDescription className="text-red-700">{error}</AlertDescription>
                </Alert>
              )}

              {solveTime && (
                <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                  <p className="text-sm text-green-700">✅ Solved in {solveTime}ms</p>
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
              <p className="mt-1">Make sure your Flask backend is running and accessible at the configured URL.</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
