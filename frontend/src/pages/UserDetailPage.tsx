import { Link, useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'

import { fetchUserById } from '../api/users'

export function UserDetailPage() {
  const { id } = useParams<{ id: string }>()
  const userId = Number(id)

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['user', userId],
    queryFn: () => fetchUserById(userId),
    enabled: !Number.isNaN(userId),
  })

  if (Number.isNaN(userId)) {
    return <p className="text-red-600">Некорректный id</p>
  }

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
      <Link to="/" className="text-sm text-blue-600 hover:underline">
        ← К списку
      </Link>
      <h1 className="text-2xl font-bold">
        {data.first_name} {data.last_name}
      </h1>

      <dl className="grid grid-cols-[max-content_1fr] gap-x-6 gap-y-2 rounded-lg border border-slate-200 bg-white p-6 text-sm shadow-sm">
        <Row label="ID" value={data.id} />
        <Row label="Пол" value={data.gender} />
        <Row label="Имя" value={data.first_name} />
        <Row label="Фамилия" value={data.last_name} />
        <Row label="Телефон" value={data.phone} />
        <Row label="Email" value={data.email} />
        <Row label="Адрес" value={data.address} />
        <Row label="Создан" value={new Date(data.created_at).toLocaleString('ru-RU')} />
      </dl>
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