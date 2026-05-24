import { Link } from "react-router-dom";
import type { User } from "../types";

interface Props {
  users: User[]
}

export function UsersTable({ users }: Props) {
  return (
    <div className="overflow-x-auto rounded-lg border border-slate-200 bg-white shadow-sm">
      <table className="w-full table-fixed divide-y divide-slate-200 text-sm">
        <colgroup>
          <col className="w-24" />        
          <col className="w-32" />        
          <col className="w-36" />        
          <col className="w-44" />        
          <col />                         
          <col />                          
          <col className="w-28" />        
        </colgroup>
        <thead className="bg-slate-100">
          <tr>
            <Th>Пол</Th>
            <Th>Имя</Th>
            <Th>Фамилия</Th>
            <Th>Телефон</Th>
            <Th>Email</Th>
            <Th>Адрес</Th>
            <Th>{''}</Th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-200">
          {users.map((u) => (
            <tr key={u.id} className="hover:bg-slate-50">
              <Td>{u.gender}</Td>
              <Td className="whitespace-nowrap">{u.first_name}</Td>
              <Td className="whitespace-nowrap">{u.last_name}</Td>
              <Td className="font-mono whitespace-nowrap">{u.phone}</Td>
              <Td className="truncate">{u.email}</Td>
              <Td className="truncate">{u.address}</Td>
              <Td>
                <Link
                  to={`/users/${u.id}`}
                  className="text-blue-600 hover:underline whitespace-nowrap"
                >
                  Подробнее
                </Link>
              </Td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function Th({ children }: { children: React.ReactNode }) {
  return (
    <th className="px-4 py-2 text-left font-semibold text-slate-700">
      {children}
    </th>
  )
}

function Td({
  children,
  className = '',
}: {
  children: React.ReactNode
  className?: string
}) {
  return <td className={`px-4 py-2 ${className}`}>{children}</td>
}