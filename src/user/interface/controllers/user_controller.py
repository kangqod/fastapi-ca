from datetime import datetime

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from containers import Container
from user.application.user_service import UserService
from user.infra.repository.user_repo import UserRepository

router = APIRouter(prefix="/users", tags=["users"])


class CreateUserBody(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    updated_at: datetime


class UpdateUserBody(BaseModel):
    name: str | None = Field(min_length=2, max_length=32, default=None)
    password: str | None = Field(min_length=8, max_length=32, default=None)


@router.post("", status_code=201)
@inject
def create_user(user: CreateUserBody, user_service: UserService = Depends(Provide["user_service"])):
    return user_service.create_user(name=user.name, email=user.email, password=user.password)


@router.get("", status_code=200)
@inject
async def get_users(page: int = 1, items_per_page: int = 10, user_service: UserService = Depends(Provide[Container.user_service])):
    total_count, users = user_service.get_users(page, items_per_page)

    return {"total_count": total_count, "page": page, "users": users}


@router.put("", response_model=UserResponse)
@inject
def update_user(user_id: str, body: UpdateUserBody, user_service: UserService = Depends(Provide["user_service"])):
    return user_service.update_user(user_id=user_id, name=body.name, password=body.password)
