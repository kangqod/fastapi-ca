from abc import ABCMeta, abstractmethod

from user.domain.user import User


class IUserRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(slef, user: User):
        raise NotImplementedError

    @abstractmethod
    def find_by_email(slef, email: str):
        """
        이메일로 유저를 검색한다.

        검색한 유저가 없을 경우 422 에러를 발생시킨다.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, user_id: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User):
        raise NotImplementedError

    @abstractmethod
    def get_users(self, page: int, items_per_page: int) -> tuple[int, list[User]]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_id: str):
        raise NotImplementedError
