from pydantic import BaseModel


class RefreshTokenDto(BaseModel):
    access_token: str
    refresh_token: str
