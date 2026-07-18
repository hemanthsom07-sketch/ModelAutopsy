import { Routes, Route } from 'react-router-dom'
import Navbar from '@/components/Navbar'
import Dashboard from '@/pages/Dashboard'

/**
 * Root app shell: persistent Navbar + routed page content.
 * Phase 4A only defines the Dashboard route - more pages can be added
 * here later without touching Navbar or the layout shell.
 */
function App() {
  return (
    <div className="min-h-screen bg-canvas bg-grid">
      <Navbar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </div>
  )
}

function NotFound() {
  return (
    <main className="mx-auto max-w-3xl px-6 py-24 text-center">
      <p className="font-mono text-sm tracking-widest text-signal">404</p>
      <h1 className="mt-2 font-display text-2xl font-semibold text-ink">
        Page not found
      </h1>
      <p className="mt-2 text-ink-soft">
        The page you&apos;re looking for doesn&apos;t exist.
      </p>
    </main>
  )
}

export default App
