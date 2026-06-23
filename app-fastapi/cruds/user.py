from sqlalchemy.ext.asyncio import AsyncSession
import schemas.user as user_schema
import models.user as user_model
from pwdlib import PasswordHash
from sqlalchemy import select

password_hash = PasswordHash.recommended()

async def add_user(
        db_session: AsyncSession,
        SignUp_data: user_schema.SignUpSchema
) -> user_model.User:
    '''
    ユーザのサインアップ
    args
        db_session: 非同期DBセッション
        SignUp_data: サインアップ時のデータ
    returns
        User: 追加したユーザーのモデル
    '''
    user_data = SignUp_data.model_dump(exclude={"password_confirm"})
    user_data["password"] = password_hash.hash(user_data["password"])
    new_User = user_model.User(**user_data)
    db_session.add(new_User)
    await db_session.commit()
    await db_session.refresh(new_User)
    return new_User

async def fetch_user_by_name(
        db_session: AsyncSession,
        user_name: str
) -> user_model.User | None:
    '''
    ユーザのログイン
    args
        db_session: 非同期DBセッション
        user_name: ユーザーの名前
    returns
        User | None: 見つかったユーザーのモデル（存在しない場合はNone）
    '''
    result = await db_session.execute(
        select(user_model.User).where(user_model.User.user_name == user_name)
    )
    user = result.scalars().first()
    return user
    
