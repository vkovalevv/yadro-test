import { apiFetch } from "./client";
import type { User, UserListResponse } from "../types";

export function fetchUsers(params: { limit: number; offset: number }) {
    const query = new URLSearchParams(
        {
            limit: String(params.limit),
            offset: String(params.offset)
        }
    )
    return apiFetch<UserListResponse>(`/users?${query}`)
}

export function fetchUserById(id: number) {
    return apiFetch<User>(`/users/${id}`)
}

export function fetchRandomUser() {
    return apiFetch<User>(`/users/random`)
}

export function loadMoreUsers(count: number) {
    return apiFetch<{ inserted: number }>(`/users/load?count=${count}`, { method: 'POST' })
}