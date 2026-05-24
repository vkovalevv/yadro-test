from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.db.session import get_session
from app.schemas import UserListResponse, UserRead

from app.external import RandomDataClient, get_random_data_client
from app.services.users import load_users

router = APIRouter(prefix='/users', tags=['users'])


@router.get('', response_model=UserListResponse)
async def list_users(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session)
) -> UserListResponse:
    total = await session.scalar(select(func.count()).select_from(User))

    result = await session.execute(
        select(User).order_by(User.id).limit(limit).offset(offset)
    )
    users = result.scalars().all()

    return UserListResponse(
        items=users,
        total=total or 0,
        limit=limit,
        offset=offset
    )


@router.get('/random', response_model=UserRead)
async def get_random_user(
    session: AsyncSession = Depends(get_session)
) -> User:
    user = await session.scalar(select(User).order_by(func.random()).limit(1))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No users in database')
    return user


@router.post('/load', status_code=status.HTTP_201_CREATED)
async def load_more_users(
    count: int = Query(..., ge=1, le=10000),
    session: AsyncSession = Depends(get_session),
    client: RandomDataClient = Depends(get_random_data_client)
) -> dict[str, int]:
    '''
    Загружаем с внешнего API указанное количество человек в нашу БД
    '''
    inserted = await load_users(session, client, count)
    return {'inserted': inserted}


@router.get('/{user_id}', response_model=UserRead)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session)
) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')
    return user
