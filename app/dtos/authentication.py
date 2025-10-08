from pydantic import BaseModel, Field, field_validator


class AuthenticationDto(BaseModel):
    email: str = Field(..., example="john.doe@example.com")

    password: str = Field(..., example="StrongP@ssw0rd")

    @field_validator("email")
    def validate_email(cls, value):
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Email inválido")
        return value

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 12:
            raise ValueError("A senha deve ter pelo menos 12 caracteres")
        if not any(c.isalpha() for c in value):
            raise ValueError("A senha deve conter pelo menos uma letra")
        if not any(c.isdigit() for c in value):
            raise ValueError("A senha deve conter pelo menos um número")
        return value
