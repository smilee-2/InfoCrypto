from pydantic import BaseModel, EmailStr


class Base(BaseModel):
    pass

# Класс для валидации пользователей
class UserModel(Base):
    email: EmailStr
    username: str
    password: str
    disabled: bool | None = None


# Класс для валидации запроса gpt
class UserInput(Base):
    user_input: str


# Класс админа
class AdminModel(UserModel):
    admin: bool


# Класс для валидации токена
class Token(Base):
    access_token: str
    token_type: str


#
class TokenData(Base):
    username: str | None = None
