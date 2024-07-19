from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, Depends, status
from src.core.db_helper import db_helper
from .hash import bcrypt 
from .models import User
from .schemas import SignUp, Token
from sqlalchemy import select
from datetime import datetime, timedelta
from .hash import verify_password
from .auth import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from .auth import ACCESS_TOKEN_EXPIRE_MINUTES




user_router = APIRouter(
    tags=['User']
)


@user_router.post('/sign-up/')
async def sign_up(request: SignUp, session: AsyncSession = Depends(db_helper.session_dependency)):
    
    hashed_password = bcrypt(request.password)

    existing_username = await session.execute(
        select(User)
        .filter(User.username == request.username)
    )

    result_for_existing_username = existing_username.scalars().first()

    if result_for_existing_username:
        raise HTTPException(detail='Username exist', status_code=403)
    



    

    new_user = User(
        username = request.username,
        password = hashed_password,
        registared_at = datetime.utcnow()
    )

    session.add(new_user)
    await session.commit()

    return new_user


@user_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(db_helper.session_dependency)):
    result = await session.execute(
        select(User).where(User.username == form_data.username)
    )
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}