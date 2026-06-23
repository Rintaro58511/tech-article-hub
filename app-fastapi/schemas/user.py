from pydantic import BaseModel, Field

class SignUpSchema(BaseModel):
    user_name: str = Field(..., min_length = 3, max_length = 50)

    password:str = Field(..., min_length=6)

    password_confirm:str = Field(..., min_length=6)

class LoginSchema(BaseModel):
    user_name: str = Field(..., min_length = 3, max_length = 50)

    password: str = Field(..., min_length=6)

class ResponseSchema(BaseModel):
    message: str = Field(...,
                         description = "API操作の結果を説明するメッセージ。",
                         example = "ユーザ認証しました")