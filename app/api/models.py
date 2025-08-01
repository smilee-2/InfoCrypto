from pydantic import BaseModel, EmailStr, ConfigDict


class Base(BaseModel):
    pass


# Класс для валидации пользователей
class UserModel(Base):
    email: EmailStr
    username: str
    password: str
    disabled: bool = False

    model_config = ConfigDict(from_attributes=True)


class UserRootModel(UserModel):
    root: str = "basic"

    model_config = ConfigDict(from_attributes=True)


class UserReturnModel(Base):
    email: EmailStr
    username: str
    root: str
    disable: bool = False

    model_config = ConfigDict(from_attributes=True)


class CoinModel(Base):
    coin_name: str
    user_id: int

    model_config = ConfigDict(from_attributes=True)


# Класс для валидации токена
class Token(Base):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
