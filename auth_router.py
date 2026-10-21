from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.params import Depends
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm
from auth import verify_password, create_access_token
from database import SessionDep
from models import User
from schemas import SUserRegister, SUser
from auth import get_password_hash

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: SUserRegister, db: SessionDep) -> SUser:
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalar_one_or_none()

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists")

    new_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password))

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(db: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    result = await db.execute(
        select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()

    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password",
                            headers={"WWW-Authenticate": "Bearer"} )

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
