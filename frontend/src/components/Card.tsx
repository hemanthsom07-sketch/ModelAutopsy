import type { ReactNode } from 'react'

interface CardProps {
  /** Small tracked-out label above the title, e.g. "DIAGNOSTICS" */
  eyebrow: string
  title: string
  /** Short status pill - defaults to the honest current state: no data yet */
  status?: string
  children?: ReactNode
}

/**
 * Shared panel used by every dashboard section so spacing, borders, and
 * the eyebrow/status treatment stay consistent across the app. Sections
 * pass their own eyebrow/title; `children` is empty for now and will
 * hold real content once a section is wired to the API.
 */
function Card({ eyebrow, title, status = 'Awaiting dataset', children }: CardProps) {
  return (
    <section className="rounded-xl border border-border bg-surface p-6 transition-colors hover:border-border-strong">
      <div className="flex items-center justify-between gap-4">
        <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-ink-faint">
          {eyebrow}
        </p>
        <span className="rounded-full border border-border px-2 py-0.5 font-mono text-[10px] text-ink-faint">
          {status}
        </span>
      </div>
      <h2 className="mt-3 font-display text-xl font-semibold text-ink">{title}</h2>
      {children && <div className="mt-4">{children}</div>}
    </section>
  )
}

export default Card
