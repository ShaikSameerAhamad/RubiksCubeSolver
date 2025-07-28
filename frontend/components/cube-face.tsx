"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"

interface CubeFaceProps {
  name: string
  colors: string
  onStickerClick: (stickerIndex: number, color: string) => void
}

const COLOR_MAP = {
  U: { bg: "bg-white", border: "border-gray-300", name: "White" },
  R: { bg: "bg-red-500", border: "border-red-600", name: "Red" },
  F: { bg: "bg-green-500", border: "border-green-600", name: "Green" },
  D: { bg: "bg-yellow-400", border: "border-yellow-500", name: "Yellow" },
  L: { bg: "bg-orange-500", border: "border-orange-600", name: "Orange" },
  B: { bg: "bg-blue-500", border: "border-blue-600", name: "Blue" },
}

const AVAILABLE_COLORS = ["U", "R", "F", "D", "L", "B"]

export function CubeFace({ name, colors, onStickerClick }: CubeFaceProps) {
  const [selectedSticker, setSelectedSticker] = useState<number | null>(null)

  const handleColorSelect = (color: string) => {
    if (selectedSticker !== null && colors && colors.length === 9) {
      onStickerClick(selectedSticker, color)
      setSelectedSticker(null)
    }
  }

  return (
    <div className="flex flex-col items-center space-y-2">
      <h3 className="text-sm font-medium text-gray-700">{name}</h3>
      <div className="grid grid-cols-3 gap-1 p-2 bg-gray-100 rounded-lg">
        {colors.split("").map((color, index) => {
          const colorInfo = COLOR_MAP[color as keyof typeof COLOR_MAP]
          return (
            <Popover key={index}>
              <PopoverTrigger asChild>
                <button
                  className={`w-8 h-8 border-2 rounded-sm transition-all hover:scale-110 ${colorInfo.bg} ${colorInfo.border} ${
                    selectedSticker === index ? "ring-2 ring-blue-500" : ""
                  }`}
                  onClick={() => setSelectedSticker(index)}
                />
              </PopoverTrigger>
              <PopoverContent className="w-48 p-2">
                <div className="grid grid-cols-3 gap-1">
                  {AVAILABLE_COLORS.map((availableColor) => {
                    const availableColorInfo = COLOR_MAP[availableColor as keyof typeof COLOR_MAP]
                    return (
                      <Button
                        key={availableColor}
                        variant="outline"
                        size="sm"
                        className={`h-8 ${availableColorInfo.bg} ${availableColorInfo.border} hover:scale-105`}
                        onClick={() => handleColorSelect(availableColor)}
                      >
                        <span className="sr-only">{availableColorInfo.name}</span>
                      </Button>
                    )
                  })}
                </div>
                <p className="text-xs text-gray-500 mt-2 text-center">Select a color for this sticker</p>
              </PopoverContent>
            </Popover>
          )
        })}
      </div>
    </div>
  )
}
