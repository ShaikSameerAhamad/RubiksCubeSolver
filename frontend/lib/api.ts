interface SolveResponse {
  success: boolean
  moves?: string[]
  error?: string
  solve_time?: number
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"

export async function solveCube(cubeState: string): Promise<SolveResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/solve`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        cube_state: cubeState,
      }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error("API Error:", error)
    return {
      success: false,
      error: "Failed to connect to the solver API",
    }
  }
}

export async function scrambleCube(): Promise<{ scramble: string }> {
  try {
    const response = await fetch(`${API_BASE_URL}/scramble`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    return data
  } catch (error) {
    console.error("Scramble API Error:", error)
    // Return a fallback scramble if API fails
    return {
      scramble: "R U R' U' R U R' F' R U R' U' R' F R",
    }
  }
}
