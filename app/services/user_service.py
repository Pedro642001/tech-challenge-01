from app.dtos.create_user_dto import CreateUserDto
from app.models.user import User
from app.services.auth_service import AuthService
from app.utils.filter import Filter


class UserService:
    def __init__(self):
        self.auth_service = AuthService()

    async def create(self, user: CreateUserDto) -> User:
        userExists = await User.filter(email=user.email).count() > 0

        if userExists:
            raise Exception("User already exists")

        user.password = self.auth_service.generate_password_hash(user.password)

        return await User.create(name=user.name, email=user.email, password_hash=user.password)

    def get_users(self, filter: Filter) -> list[User]:
        return User.all().order_by(filter.order_by).offset(filter.offset).limit(filter.limit)

    async def get_user_by_email(self, email: str) -> User | None:
        return await User.filter(email=email).get_or_none()
