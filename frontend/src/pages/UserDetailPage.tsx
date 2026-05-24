import { useParams } from 'react-router-dom'

export function UserDetailPage() {
  const { id } = useParams()
  return <h1 className="text-2xl font-bold">Пользователь #{id}</h1>
}