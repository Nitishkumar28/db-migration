from pydantic import BaseModel, EmailStr, constr, model_validator

class SignUpRequest(BaseModel):
    first_name: constr(min_length=1)
    last_name:  constr(min_length=1)
    email:      EmailStr
    password:   constr(min_length=8)
    password_confirm: str

    @model_validator(mode='before')
    def passwords_match(cls, values: dict):
        if values.get("password") != values.get("password_confirm"):
            raise ValueError("Passwords do not match")
        return values
    
class LoginRequest(BaseModel):
    email: EmailStr  
    password:   str

class TokenRequest(BaseModel):
    access_token: str
    token_type:   str = "bearer"