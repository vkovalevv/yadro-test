import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'

import { loadMoreUsers } from '../api/users'

export function LoadUsersForm() {
  const [count, setCount] = useState(10)
  const queryClient = useQueryClient()

  const mutation = useMutation({
    mutationFn: (n: number) => loadMoreUsers(n),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] })
    },
  })

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault()
        mutation.mutate(count)
      }}
      className="flex items-end gap-3 rounded-lg border border-slate-200 bg-white p-4 shadow-sm"
    >
      <label className="flex flex-col gap-1 text-sm">
        <span className="font-medium text-slate-700">Загрузить с API</span>
        <input
          type="number"
          min={1}
          max={10000}
          value={count}
          onChange={(e) => setCount(Number(e.target.value))}
          className="w-32 rounded border border-slate-300 px-3 py-1.5 focus:border-blue-500 focus:outline-none"
        />
      </label>
      <button
        type="submit"
        disabled={mutation.isPending}
        className="rounded bg-blue-600 px-4 py-1.5 font-medium text-white
                   hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {mutation.isPending ? 'Загрузка…' : 'Загрузить'}
      </button>

      {mutation.isSuccess && (
        <span className="text-sm text-green-600">
          Загружено: {mutation.data.inserted}
        </span>
      )}
      {mutation.isError && (
        <span className="text-sm text-red-600">
          Ошибка:{' '}
          {mutation.error instanceof Error ? mutation.error.message : 'неизвестная'}
        </span>
      )}
    </form>
  )
}