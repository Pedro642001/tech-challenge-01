from pydantic import BaseModel, Field


class AccessTokenDto(BaseModel):
    """
    DTO de resposta que contém os tokens de autenticação do usuário.
    Retornado após o login ou a renovação de sessão.
    """

    access_token: str = Field(
        ...,
        description="Token JWT de acesso com tempo de expiração curto (ex: 15 minutos).",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    )
    refresh_token: str = Field(
        ...,
        description="Token usado para renovar o access token quando este expira.",
        example="dGhpc2lzYXJlZnJlc2h0b2tlbg==",
    )
    token_type: str = Field(
        description="Tipo do token de autenticação. Normalmente 'Bearer'.", examples=["Bearer"]
    )
    expires_in: int = Field(
        example=900, description="Tempo de expiração do access token, em segundos."
    )
