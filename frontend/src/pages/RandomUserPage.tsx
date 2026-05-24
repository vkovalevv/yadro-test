import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'

import { fetchRandomUser } from '../api/users'

export function RandomUserPage() {
  const { data, isLoading, isError, error, refetch, isFetching } = useQuery({
    queryKey: ['user', 'random'],
    queryFn: fetchRandomUser,
    staleTime: 0,
    gcTime: 0,
    refetchOnMount: 'always',
  })

  if (isLoading) return <p className="text-slate-500">Загрузка…</p>

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
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Случайный пользователь</h1>
        <button
          onClick={() => refetch()}
          disabled={isFetching}
          className="rounded border border-slate-300 bg-white px-3 py-1.5 text-sm font-medium
                     hover:bg-slate-50 disabled:opacity-50"
        >
          {isFetching ? 'Обновляю…' : 'Другой случайный'}
        </button>
      </div>

      <dl className="grid grid-cols-[max-content_1fr] gap-x-6 gap-y-2 rounded-lg border border-slate-200 bg-white p-6 text-sm shadow-sm">
        <Row label="ID" value={data.id} />
        <Row label="Пол" value={data.gender} />
        <Row label="Имя" value={data.first_name} />
        <Row label="Фамилия" value={data.last_name} />
        <Row label="Телефон" value={data.phone} />
        <Row label="Email" value={data.email} />
        <Row label="Адрес" value={data.address} />
      </dl>

      <Link to={`/users/${data.id}`} className="text-sm text-blue-600 hover:underline">
        К странице пользователя →
      </Link>
    </div>
  )
}

function Row({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <>
      <dt className="font-medium text-slate-500">{label}</dt>
      <dd className="text-slate-900">{value}</dd>
    </>
  )
}