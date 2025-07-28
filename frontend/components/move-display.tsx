"use client"

import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Copy, RotateCw } from "lucide-react"
import { useState } from "react"

interface MoveDisplayProps {
  moves: string[]
}

export function MoveDisplay({ moves }: MoveDisplayProps) {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null)

  const copyToClipboard = (text: string, index?: number) => {
    navigator.clipboard.writeText(text)
    if (index !== undefined) {
      setCopiedIndex(index)
      setTimeout(() => setCopiedIndex(null), 2000)
    }
  }

  const copyAllMoves = () => {
    const allMoves = moves.join(" ")
    copyToClipboard(allMoves)
  }

  if (moves.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <RotateCw className="w-12 h-12 mx-auto mb-4 opacity-50" />
        <p>No solution yet. Configure your cube and click "Solve Cube" to get started.</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="font-semibold text-gray-900">Solution Steps</h3>
          <p className="text-sm text-gray-600">{moves.length} moves total</p>
        </div>
        <Button variant="outline" size="sm" onClick={copyAllMoves} className="flex items-center gap-2 bg-transparent">
          <Copy className="w-4 h-4" />
          Copy All
        </Button>
      </div>

      <Card>
        <CardContent className="p-4">
          <div className="flex flex-wrap gap-2">
            {moves.map((move, index) => (
              <Badge
                key={index}
                variant="secondary"
                className="text-sm px-3 py-1 cursor-pointer hover:bg-gray-200 transition-colors"
                onClick={() => copyToClipboard(move, index)}
              >
                {move}
                {copiedIndex === index && <span className="ml-1 text-xs text-green-600">✓</span>}
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>

      <div className="text-xs text-gray-500 space-y-1">
        <p>
          <strong>Move Notation:</strong>
        </p>
        <p>• F/B/R/L/U/D = Front/Back/Right/Left/Up/Down face clockwise</p>
        <p>• ' = Counter-clockwise (e.g., F')</p>
        <p>• 2 = Double turn (e.g., F2)</p>
      </div>
    </div>
  )
}
