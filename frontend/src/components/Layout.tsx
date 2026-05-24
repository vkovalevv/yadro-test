import { Link, Outlet } from 'react-router-dom'

export function Layout() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto max-w-6xl px-6 py-4 flex items-center gap-6">
          <Link to="/" className="text-xl font-semibold">
            Users Directory
          </Link>
          <nav className="flex gap-4 text-sm">
            <Link to="/" className="hover:underline">Список</Link>
            <Link to="/random" className="hover:underline">Случайный</Link>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-6 py-8">
        <Outlet />
      </main>
    </div>
  )
}