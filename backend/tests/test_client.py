import httpx
import respx
import pytest

from app.external import RandomDataClient

BASE_URL = 'https://api.example.test/'


def _make_user(first_name: str = 'Иван') -> dict:
    return {
        'FirstName': first_name,
        'LastName': 'Иванов',
        'Gender': 'Мужчина',
        'Phone': '+7 (999) 123-45-67',
        'Email': 'ivanov@example.com',
        'Address': 'Россия, г. Москва, ул. Ленина, д. 1'
    }


@respx.mock
async def test_fetch_users_parses_response():
    respx.get(BASE_URL).mock(
        return_value=httpx.Response(
            200, json=[_make_user('Иван'), _make_user('Петр')])
    )

    client = RandomDataClient(base_url=BASE_URL)
    users = await client.fetch_users(2)

    assert len(users) == 2
    assert users[0].first_name == 'Иван'
    assert users[1].first_name == 'Петр'
    assert users[0].address == 'Россия, г. Москва, ул. Ленина, д. 1'


@respx.mock
async def test_fetch_users_handles_single_object_response():
    respx.get(BASE_URL).mock(
        return_value=httpx.Response(200, json=_make_user()))

    client = RandomDataClient(base_url=BASE_URL)
    users = await client.fetch_users(1)

    assert len(users) == 1
    assert users[0].first_name == 'Иван'


@respx.mock
async def test_fetch_users_batches_requests_count_exceeds_limit():
    route = respx.get(BASE_URL).mock(
        return_value=httpx.Response(200, json=[_make_user()]*100)
    )
    client = RandomDataClient(base_url=BASE_URL)
    users = await client.fetch_users(250)
    assert len(users) == 250
    assert route.call_count == 3  # 100+100+50
    last_request = route.calls[-1].request
    assert last_request.url.params['count'] == '50'


@respx.mock
async def test_fetch_users_raises_on_http_error():
    respx.get(BASE_URL).mock(return_value=httpx.Response(500))

    client = RandomDataClient(base_url=BASE_URL)

    with pytest.raises(httpx.HTTPStatusError):
        await client.fetch_users(1)


@respx.mock
async def test_fetch_usesrs_truncates_api_returns_extra():
    respx.get(BASE_URL).mock(
        return_value=httpx.Response(200, json=[_make_user()]*100))

    client = RandomDataClient(base_url=BASE_URL)
    users = await client.fetch_users(5)
    assert len(users) == 5


@respx.mock
async def test_fetch_users_stops_api_return_empty():
    respx.get(BASE_URL).mock(return_value=httpx.Response(200, json=[]))

    client = RandomDataClient(base_url=BASE_URL)
    users = await client.fetch_users(50)

    assert users == []


async def test_fetch_users_returns_empty_for_zero_count():
    client = RandomDataClient(base_url=BASE_URL)
    users = await client.fetch_users(0)
    assert users == []
