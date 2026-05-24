import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

import { Layout } from './components/Layout'
import { UsersListPage } from './pages/UsersListPage'
import { UserDetailPage } from './pages/UserDetailPage'
import { RandomUserPage } from './pages/RandomUserPage'

import './index.css'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
})

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<UsersListPage />} />
            <Route path="users/:id" element={<UserDetailPage />} />
            <Route path="random" element={<RandomUserPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  </StrictMode>,
)