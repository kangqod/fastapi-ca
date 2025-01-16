from datetime import datetime
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field

from common.auth import CurrentUser, get_current_user
from containers import Container
from user.application.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


class CreateUserBody(BaseModel):
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    password: str = Field(min_length=8, max_length=32)


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    updated_at: datetime


class GetUserResponse(BaseModel):
    total_count: int
    page: int
    users: list[UserResponse]


class UpdateUserBody(BaseModel):
    name: str | None = Field(min_length=2, max_length=32, default=None)
    password: str | None = Field(min_length=8, max_length=32, default=None)


@router.post("", status_code=201, response_model=UserResponse)
@inject
def create_user(user: CreateUserBody, user_service: UserService = Depends(Provide["user_service"])):
    return user_service.create_user(name=user.name, email=user.email, password=user.password)


@router.get("", status_code=200)
@inject
async def get_users(
    page: int = 1,
    items_per_page: int = 10,
    current_user: CurrentUser = Depends(get_current_user),
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    total_count, users = user_service.get_users(page, items_per_page)
    user_responses = [UserResponse(id=user.id, name=user.name, email=user.email, created_at=user.created_at, updated_at=user.updated_at) for user in users]

    return GetUserResponse(total_count=total_count, page=page, users=user_responses)


@router.put("", response_model=UserResponse)
@inject
def update_user(
    current_user: Annotated[CurrentUser, Depends(get_current_user)], body: UpdateUserBody, user_service: UserService = Depends(Provide["user_service"])
):
    return user_service.update_user(user_id=current_user.id, name=body.name, password=body.password)


@router.delete("", status_code=204)
@inject
def delete_user(current_user: Annotated[CurrentUser, Depends(get_current_user)], user_service: UserService = Depends(Provide[Container.user_service])):
    # 다른 유저를 삭제할 수 없도록 토큰에서 유저아이디를 구함
    return user_service.delete_user(user_id=current_user.id)


@router.post("/login", status_code=200)
@inject
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], user_service: UserService = Depends(Provide[Container.user_service])):
    access_token = user_service.login(email=form_data.username, password=form_data.password)

    return {"access_token": access_token, "token_type": "bearer"}
