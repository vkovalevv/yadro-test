# Users Directory

Web-приложение для работы со списком случайных пользователей.
При старте бэкенд загружает 1000 человек с публичного API
[randomdatatools.ru](https://api.randomdatatools.ru/) и складывает в БД.

## Стeк

- **FastAPI** — современный async-фреймворк, из коробки даёт автогенерацию OpenAPI и удобную систему зависимостей (`Depends`), что упрощает и эндпоинты, и тесты.
- **PostgreSQL + SQLAlchemy 2.0 (async)** — стандартная production-связка. Async-движок естественно сочетается с async-кодом FastAPI.
- **Alembic** — миграции схемы.
- **httpx** — async HTTP-клиент для запросов во внешний API; `respx` мокает его в тестах.
- **React + Vite + TypeScript** — быстрый dev-сервер, статическая типизация.
- **TanStack Query** — управление server state: кэширование, состояния loading/error, инвалидация.
- **Tailwind CSS** — быстрая разработка UI без отдельных CSS-файлов.

## Запуск

```bash
git clone <url> yadro-test
cd yadro-test
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Swagger: http://localhost:8000/docs

При первом старте применяются миграции и подтягивается 1000 пользователей.

## Локальный запуск для разработки

### Поднять Postgres

```bash
docker run -d --name yadro-pg \
  -e POSTGRES_USER=app -e POSTGRES_PASSWORD=app -e POSTGRES_DB=app \
  -p 5433:5432 postgres:16-alpine

docker exec -it yadro-pg psql -U app -d app -c "CREATE DATABASE app_test;"
```

### Backend

```bash
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Тесты

Нужен запущенный Postgres c БД `app_test` (см. выше).

```bash
cd backend
pytest -v
```

Тесты внешнего API замоканы через `respx`.

## API

| Метод | Путь | Описание |
|---|---|---|
| GET | `/users?limit=&offset=` | Список с пагинацией |
| GET | `/users/{id}` | Один пользователь |
| GET | `/users/random` | Случайный пользователь из БД |
| POST | `/users/load?count=N` | Дозагрузить N пользователей с внешнего API |

Интерактивная документация: `/docs`.

## Структура

```
backend/   FastAPI + SQLAlchemy + Alembic
frontend/  React + Vite + TS
```