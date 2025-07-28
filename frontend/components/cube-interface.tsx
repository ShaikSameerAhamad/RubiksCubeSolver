"use client"

import { CubeFace } from "./cube-face"

interface CubeInterfaceProps {
  cubeState: string
  onStateChange: (newState: string) => void
}

export function CubeInterface({ cubeState, onStateChange }: CubeInterfaceProps) {
  const updateSticker = (faceIndex: number, stickerIndex: number, color: string) => {
    if (!cubeState || cubeState.length !== 54) {
      console.error('Invalid cube state');
      return;
    }
    const globalIndex = faceIndex * 9 + stickerIndex
    const newState = cubeState.split("")
    newState[globalIndex] = color
    const updatedState = newState.join("")
    if (updatedState.length === 54) {
      onStateChange(updatedState)
    }
  }

  // Extract face states from the 54-character string
  const faces = [
    { name: "Up", colors: cubeState.slice(0, 9), index: 0 },
    { name: "Right", colors: cubeState.slice(9, 18), index: 1 },
    { name: "Front", colors: cubeState.slice(18, 27), index: 2 },
    { name: "Down", colors: cubeState.slice(27, 36), index: 3 },
    { name: "Left", colors: cubeState.slice(36, 45), index: 4 },
    { name: "Back", colors: cubeState.slice(45, 54), index: 5 },
  ]

  return (
    <div className="space-y-6">
      {/* Top row - Up face */}
      <div className="flex justify-center">
        <CubeFace
          name={faces[0].name}
          colors={faces[0].colors}
          onStickerClick={(stickerIndex, color) => updateSticker(faces[0].index, stickerIndex, color)}
        />
      </div>

      {/* Middle row - Left, Front, Right, Back */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <CubeFace
          name={faces[4].name}
          colors={faces[4].colors}
          onStickerClick={(stickerIndex, color) => updateSticker(faces[4].index, stickerIndex, color)}
        />
        <CubeFace
          name={faces[2].name}
          colors={faces[2].colors}
          onStickerClick={(stickerIndex, color) => updateSticker(faces[2].index, stickerIndex, color)}
        />
        <CubeFace
          name={faces[1].name}
          colors={faces[1].colors}
          onStickerClick={(stickerIndex, color) => updateSticker(faces[1].index, stickerIndex, color)}
        />
        <CubeFace
          name={faces[5].name}
          colors={faces[5].colors}
          onStickerClick={(stickerIndex, color) => updateSticker(faces[5].index, stickerIndex, color)}
        />
      </div>

      {/* Bottom row - Down face */}
      <div className="flex justify-center">
        <CubeFace
          name={faces[3].name}
          colors={faces[3].colors}
          onStickerClick={(stickerIndex, color) => updateSticker(faces[3].index, stickerIndex, color)}
        />
      </div>
    </div>
  )
}
