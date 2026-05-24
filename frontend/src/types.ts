export interface User {
    id: number
    first_name: string
    last_name: string
    gender: string
    phone: string
    email: string
    address: string
    created_at: string
}

export interface UserListResponse {
    items: User[]
    total: number
    limit: number
    offset: number
}