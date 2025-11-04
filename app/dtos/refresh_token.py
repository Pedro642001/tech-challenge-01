from pydantic import BaseModel, Field


class RefreshTokenDto(BaseModel):
    access_token: str = Field(
        ...,
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        description="Token JWT de acesso com tempo de expiração curto (ex: 15 minutos).",
    )
    refresh_token: str = Field(
        ...,
        example="dGhpc2lzYXJlZnJlc2h0b2tlbg==",
        description="Token usado para renovar o access token quando este expira.",
    )
