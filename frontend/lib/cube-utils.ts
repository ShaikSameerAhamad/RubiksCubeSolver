// Utility functions for cube state manipulation

export function generateScrambledState(): string {
  // Generate a random scrambled cube state
  // This is a simplified scramble - in a real implementation,
  // you'd want to apply actual scramble moves to a solved state
  const colors = ["U", "R", "F", "D", "L", "B"]
  const scrambledState = []

  // Ensure each color appears exactly 9 times (valid cube)
  for (let i = 0; i < 6; i++) {
    for (let j = 0; j < 9; j++) {
      scrambledState.push(colors[i])
    }
  }

  // Shuffle the array while maintaining cube validity
  // This is a basic shuffle - real scrambling should use proper cube moves
  for (let i = scrambledState.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[scrambledState[i], scrambledState[j]] = [scrambledState[j], scrambledState[i]]
  }

  return scrambledState.join("")
}

export function isValidCubeState(cubeState: string): boolean {
  if (cubeState.length !== 54) return false

  const colorCounts: { [key: string]: number } = {}
  const validColors = ["U", "R", "F", "D", "L", "B"]

  for (const color of cubeState) {
    if (!validColors.includes(color)) return false
    colorCounts[color] = (colorCounts[color] || 0) + 1
  }

  // Each color should appear exactly 9 times
  for (const color of validColors) {
    if (colorCounts[color] !== 9) return false
  }

  return true
}

export function formatMoves(moves: string[]): string {
  return moves.join(" ")
}

export function parseMoves(moveString: string): string[] {
  return moveString
    .trim()
    .split(/\s+/)
    .filter((move) => move.length > 0)
}
