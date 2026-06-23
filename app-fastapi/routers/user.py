from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import LoginSchema, SignUpSchema, ResponseSchema
import cruds.user as user_crud
from pwdlib import PasswordHash
import db

router = APIRouter(tags=["User"], prefix="/user")
password_hash = PasswordHash.recommended()

@router.post("/signup", response_model = ResponseSchema)
async def sign_up(user: SignUpSchema, db: AsyncSession = Depends(db.get_db_session)):
    existing_user = await user_crud.fetch_user_by_name(db, user.user_name)
    
    if existing_user is not None:
        raise HTTPException(
            status_code= 409, 
            detail="その名前はすでに使われています"
        )
    
    try:
        await user_crud.add_user(db, user)
        return ResponseSchema(message = "ユーザーが登録されました")
    except Exception as e:
        raise HTTPException(status_code=400, detail="ユーザーの登録に失敗しました。")

@router.post("/login", response_model = ResponseSchema)
async def login(user: LoginSchema, db: AsyncSession = Depends(db.get_db_session)):

    try:
        existing_user = await user_crud.fetch_user_by_name(db, user.user_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail="データベースエラーが発生しました。")

    if existing_user is None:
        raise HTTPException(status_code = 400, detail = "ユーザー名かパスワードが間違っています")
    
    is_password_correct = password_hash.verify(user.password, existing_user.password)
    
    if not is_password_correct:
        raise HTTPException(status_code = 400, detail = "ユーザー名かパスワードが間違っています")
    
    return ResponseSchema(message = "ログインしました")