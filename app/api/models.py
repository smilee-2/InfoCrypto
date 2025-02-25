from pydantic import BaseModel, EmailStr, ConfigDict


class Base(BaseModel):
    pass


# Класс для валидации пользователей
class UserModel(Base):
    email: EmailStr
    username: str
    password: str
    disabled: bool = False
    root: str = 'basic'
    model_config = ConfigDict(from_attributes=True)

# Класс для валидации токена
class Token(Base):
    access_token: str
    token_type: str


#
class TokenData(Base):
    username: str | None = None
