from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import schemas.favorite as favorite_schema
import models.favorite as favorite_model
import logging

async def add_favorite(
        db_session: AsyncSession,
        Favorite_data: favorite_schema.FavoriteSchema
) -> favorite_model.Favorite:
    '''
    新しい記事をお気に入りに追加
    args
        db_session: 非同期DBセッション
        Favorite_data: 追加する記事のデータ
    returns
        Favorite: 追加した記事のモデル
    '''
    try:
        new_Favorite = favorite_model.Favorite(**Favorite_data.model_dump())
        db_session.add(new_Favorite)
        await db_session.commit()
        await db_session.refresh(new_Favorite)
        return new_Favorite
    except Exception as e:
        logging.error(f"データベース登録中にエラーが発生しました:{e}")
        raise e

async def list_favorite(db_session: AsyncSession) -> list[favorite_model.Favorite]:
    '''
    お気に入り記事の一覧表示
    args
        db_session: 非同期DBセッション
    returns
         list[Favorite]
    '''
    result = await db_session.execute(select(favorite_model.Favorite))
    Favorites = result.scalars().all()
    return Favorites

async def delete_favorite(
        db_session: AsyncSession,
        Favorite_id: int
) -> favorite_model.Favorite | None:
    '''
    お気に入り記事の削除
    args
        db_sessoin: 非同期DBセッション
        Favorite_id: 削除する記事のID
    return
        削除した記事
    '''
    result = await db_session.execute(select(favorite_model.Favorite)
                                        .where(favorite_model.Favorite.id == Favorite_id))
    favorite = result.scalar_one_or_none()
    if favorite:
        await db_session.delete(favorite)
        await db_session.commit()
    
    return favorite
