// lib/cube-utils.ts

/**
 * Utility functions for Rubik's cube operations
 */

import { solveCube, scrambleCube } from './api';

export async function generateScrambledState(): Promise<string> {
  try {
    const { scramble } = await scrambleCube();
    return scramble;
  } catch (error) {
    console.error('Failed to get scramble from API:', error);
    throw error;
  }
}

export function isValidCubeState(state: string): boolean {
  // Check if the state is 54 characters long and only contains valid face colors
  return state.length === 54 && /^[UDLRFB]+$/.test(state);
}
