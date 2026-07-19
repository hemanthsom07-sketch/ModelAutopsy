import { useMemo } from 'react'
import { ResponsiveContainer, Scatter, ScatterChart, Tooltip, XAxis, YAxis } from 'recharts'
import type { ScatterShapeProps } from 'recharts/types/util/ScatterUtils'
import ChartPanel from '@/components/charts/ChartPanel'
import type { CorrelationHeatmapData } from '@/services/api'

interface CorrelationHeatmapProps {
  data: CorrelationHeatmapData | null
}

interface HeatCell {
  x: string
  y: string
  value: number | null
}

// Kept in sync with the --color-* tokens in index.css. Recharts renders
// SVG, and a plain rgb() interpolation is more predictable inside an SVG
// fill than relying on color-mix() being parsed correctly there.
const SURFACE_RGB: [number, number, number] = [18, 22, 31]
const SIGNAL_RGB: [number, number, number] = [69, 214, 196]
const CRITICAL_RGB: [number, number, number] = [229, 85, 92]

function mixColor(from: [number, number, number], to: [number, number, number], t: number): string {
  const r = Math.round(from[0] + (to[0] - from[0]) * t)
  const g = Math.round(from[1] + (to[1] - from[1]) * t)
  const b = Math.round(from[2] + (to[2] - from[2]) * t)
  return `rgb(${r}, ${g}, ${b})`
}

function correlationColor(value: number | null): string {
  if (value === null) return 'rgb(35, 41, 55)' // border color - marks an undefined cell
  const intensity = Math.min(Math.abs(value), 1)
  return value >= 0
    ? mixColor(SURFACE_RGB, SIGNAL_RGB, intensity)
    : mixColor(SURFACE_RGB, CRITICAL_RGB, intensity)
}

/** Renders one filled square per cell, centered on Recharts' computed point position. */
function HeatmapCell(props: ScatterShapeProps) {
  const { cx, cy, payload } = props
  if (cx === undefined || cy === undefined) return null
  const size = 22
  const cell = payload as HeatCell
  return (
    <rect
      x={cx - size / 2}
      y={cy - size / 2}
      width={size}
      height={size}
      rx={2}
      fill={correlationColor(cell.value)}
    />
  )
}

/**
 * Correlation matrix as a heatmap. Recharts has no built-in heatmap chart
 * type, so this builds one from ScatterChart: every (row, column) pair
 * becomes a scatter point on categorical axes, rendered as a colored
 * square via a custom shape instead of the default circle marker.
 */
function CorrelationHeatmap({ data }: CorrelationHeatmapProps) {
  const cells: HeatCell[] = useMemo(() => {
    if (!data) return []
    const result: HeatCell[] = []
    data.labels.forEach((rowLabel, rowIndex) => {
      data.labels.forEach((colLabel, colIndex) => {
        const value = data.matrix[rowIndex]?.[colIndex];  

result.push({
  x: colLabel,
  y: rowLabel,
  value: value ?? null,
});
      })
    })
    return result
  }, [data])

  const isEmpty = !data || data.labels.length < 2

  return (
    <ChartPanel
      title="Correlation heatmap"
      isEmpty={isEmpty}
      emptyMessage="Need at least 2 numeric columns to compute correlation"
    >
      <ResponsiveContainer width="100%" height="100%">
        <ScatterChart margin={{ top: 4, right: 16, left: 8, bottom: 24 }}>
          <XAxis
            type="category"
            dataKey="x"
            name="column"
            allowDuplicatedCategory={false}
            tick={{ fontSize: 9, fill: 'var(--color-ink-faint)' }}
            angle={-35}
            textAnchor="end"
            interval={0}
            height={60}
          />
          <YAxis
            type="category"
            dataKey="y"
            name="column"
            allowDuplicatedCategory={false}
            tick={{ fontSize: 9, fill: 'var(--color-ink-faint)' }}
            width={90}
          />
          <Tooltip
  cursor={{ strokeDasharray: "3 3" }}
  content={({ active, payload }) => {
    if (!active || !payload || payload.length === 0) {
      return null;
    }

    const cell = payload[0].payload as HeatCell;

    return (
      <div
        style={{
          background: "var(--color-surface)",
          border: "1px solid var(--color-border)",
          borderRadius: 8,
          padding: "10px 12px",
          color: "var(--color-ink)",
          fontSize: 12,
        }}
      >
        <div style={{ fontWeight: 600, marginBottom: 6 }}>
          {cell.y}
        </div>

        <div style={{ marginBottom: 4 }}>
          <strong>vs</strong> {cell.x}
        </div>

        <div>
          <strong>Correlation:</strong>{" "}
          {cell.value !== null
            ? cell.value.toFixed(2)
            : "N/A"}
        </div>
      </div>
    );
  }}
/>
          <Scatter data={cells} shape={HeatmapCell} isAnimationActive={false} />
        </ScatterChart>
      </ResponsiveContainer>
    </ChartPanel>
  )
}

export default CorrelationHeatmap
