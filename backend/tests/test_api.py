from httpx import AsyncClient
import httpx
import respx
from app.db.models import User


async def test_list_users_empty(client: AsyncClient):
    response = await client.get('/users')
    assert response.status_code == 200
    assert response.json() == {'items': [], 'total': 0,
                               'limit': 50, 'offset': 0}


async def test_list_users_returns_seeded(client: AsyncClient, seeded_users: list[User]):
    response = await client.get('/users')
    assert response.status_code == 200
    body = response.json()
    assert body['total'] == 5
    assert len(body['items']) == 5


async def test_list_users_pagination(client: AsyncClient, seeded_users: list[User]):
    response = await client.get('/users', params={'limit': 2, 'offset': 2})
    assert response.status_code == 200
    body = response.json()
    assert len(body['items']) == 2
    assert body['limit'] == 2
    assert body['offset'] == 2
    assert body['total'] == 5


async def test_get_user_by_id(client: AsyncClient, seeded_users: list[User]):
    user_id = seeded_users[0].id
    response = await client.get(f'/users/{user_id}')
    assert response.status_code == 200
    assert response.json()['id'] == user_id


async def test_get_user_not_found(client: AsyncClient):
    response = await client.get('/users/9999999')
    assert response.status_code == 404


async def test_get_random_user_returns_404_when_db_empty(client: AsyncClient):
    response = await client.get('/users/random')
    assert response.status_code == 404


async def test_get_random_user_returns_existing_user(
    client: AsyncClient, seeded_users: list[User]
):
    response = await client.get('/users/random')
    assert response.status_code == 200
    seeded_ids = {user.id for user in seeded_users}
    assert response.json()['id'] in seeded_ids


async def test_random_user_eventually_varies(
    client: AsyncClient, seeded_users: list[User]
):
    ids: set[int] = set()
    for _ in range(10):
        response = await client.get('/users/random')
        ids.add(response.json()['id'])
    assert len(ids) > 1, 'random return the same user 10 times'


@respx.mock
async def test_load_more_users_insert_into_db(client: AsyncClient):
    user_payload = {
        'FirstName': 'Иван',
        'LastName': 'Иванов',
        'Gender': 'Мужчина',
        'Phone': '+7 (999) 000-00-00',
        'Email': 'ivan@test.com',
        'Address': 'Россия, г. Москва'
    }
    respx.get('https://api.randomdatatools.ru/').mock(
        return_value=httpx.Response(200, json=[user_payload]*3)
    )

    response = await client.post('/users/load', params={'count': 3})

    assert response.status_code == 201
    assert response.json() == {'inserted': 3}

    list_response = await client.get('/users')
    assert list_response.json()['total'] == 3
