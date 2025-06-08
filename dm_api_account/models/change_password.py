from pydantic import BaseModel, Field, ConfigDict



class ChangePassword(BaseModel):
    login: str = Field(..., description="Логин")
    token: str = Field(..., description="Токен сброса пароля")
    oldPassword: str = Field(..., description="Старый пароль")
    newPassword: str = Field(..., description="Новый пароль")