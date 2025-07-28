// lib/api.ts

// The base URL for your backend API, read from environment variables
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * A more robust fetch handler that properly catches all error types.
 * @param endpoint - The API endpoint to call.
 * @param options - The options for the fetch request.
 * @returns An object with the data or an error message.
 */
async function apiFetch(endpoint: string, options: RequestInit = {}) {
  try {
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    // If the response is not OK, we need to handle the error carefully
    if (!response.ok) {
      const contentType = response.headers.get("content-type");
      let errorDetail = `Request failed with status: ${response.status}`;

      // Try to parse a detailed error message from the backend if it's JSON
      if (contentType && contentType.includes("application/json")) {
        const errorJson = await response.json();
        errorDetail = errorJson.detail || errorJson.message || errorDetail;
      } else {
        // If the response is not JSON (e.g., an HTML error page), get the text
        const errorText = await response.text();
        // Avoid showing a huge HTML page in the error message
        errorDetail = `Server returned a non-JSON response. Status: ${response.status}.`;
      }
      return { success: false, error: errorDetail };
    }

    // If the response is OK, parse the JSON data
    const data = await response.json();
    return { success: true, data };

  } catch (error) {
    // This will catch network errors and the errors thrown above
    console.error(`API call to ${endpoint} failed:`, error);
    const errorMessage = error instanceof Error ? error.message : "An unknown error occurred.";
    return { success: false, error: errorMessage };
  }
}

/**
 * Calls the backend to solve the cube.
 * @param cubeState - The 54-character string representing the cube.
 */
export async function solveCube(cubeState: string) {
  console.log('Solving cube state:', cubeState);
  const result = await apiFetch('/solve', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ state: cubeState }),
  });

  if (!result.success) {
    throw new Error(result.error || 'Failed to solve cube');
  }

  if (!result.data || !result.data.solution) {
    throw new Error('Invalid response from solver');
  }

  return result;
}

/**
 * Calls the backend to get a random scramble.
 * @returns A promise that resolves to the scramble data.
 */
export async function scrambleCube() {
  const result = await apiFetch('/scramble');
  if (!result.success) {
    throw new Error(result.error || 'Failed to generate scramble');
  }
  if (!result.data || !result.data.scrambled_state || result.data.scrambled_state.length !== 54) {
    throw new Error('Invalid scramble state received from server');
  }
  return result.data;
}
