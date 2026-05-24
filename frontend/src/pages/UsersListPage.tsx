import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'

import { fetchUsers } from '../api/users'
import { UsersTable } from '../components/UsersTable'
import { Pagination } from '../components/Pagination'

import { LoadUsersForm } from '../components/LoadUsersForm'

const PAGE_SIZE = 20

export function UsersListPage() {
  const [page, setPage] = useState(0)

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['users', { limit: PAGE_SIZE, offset: page * PAGE_SIZE }],
    queryFn: () => fetchUsers({ limit: PAGE_SIZE, offset: page * PAGE_SIZE }),
    placeholderData: (prev) => prev,  // не моргать пустым экраном при переключении страниц
  })

  if (isLoading && !data) {
    return <p className="text-slate-500">Загрузка…</p>
  }

  if (isError) {
    return (
      <p className="text-red-600">
        Ошибка: {error instanceof Error ? error.message : 'неизвестная'}
      </p>
    )
  }

  if (!data) return null

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">
        Пользователи{' '}
        <span className="text-slate-500 text-base font-normal">({data.total})</span>
      </h1>
      <LoadUsersForm />
      <UsersTable users={data.items} />
      <Pagination
        page={page}
        pageSize={PAGE_SIZE}
        total={data.total}
        onChange={setPage}
      />
    </div>
  )
}