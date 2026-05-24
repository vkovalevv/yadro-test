interface Props {
  page: number
  pageSize: number
  total: number
  onChange: (page: number) => void
}

export function Pagination({ page, pageSize, total, onChange }: Props) {
  const totalPages = Math.max(1, Math.ceil(total / pageSize))
  const canPrev = page > 0
  const canNext = page < totalPages - 1

  return (
    <div className="flex items-center justify-between text-sm">
      <span className="text-slate-600">
        Страница {page + 1} из {totalPages}
      </span>
      <div className="flex gap-2">
        <Button disabled={!canPrev} onClick={() => onChange(page - 1)}>
          ← Назад
        </Button>
        <Button disabled={!canNext} onClick={() => onChange(page + 1)}>
          Вперёд →
        </Button>
      </div>
    </div>
  )
}

function Button({
  children,
  disabled,
  onClick,
}: {
  children: React.ReactNode
  disabled?: boolean
  onClick: () => void
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="rounded border border-slate-300 bg-white px-3 py-1.5 font-medium
                 hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed"
    >
      {children}
    </button>
  )
}