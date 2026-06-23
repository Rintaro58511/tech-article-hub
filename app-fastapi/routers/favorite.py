from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.favorite import FavoriteSchema, ResponseSchema
from . import ai_model
import cruds.favorite as favorite_crud
import db
import httpx
import logging

router = APIRouter(tags=["Favorite"], prefix="/favorite")

@router.get("/search", response_model=list[dict])
async def search_qiita_articles(key_word: str = ""):
    
    if key_word:
        url = f"https://qiita.com/api/v2/items?query={key_word}&sort=count&per_page=5"
    else:
        url = "https://qiita.com/api/v2/items?query=python&per_page=5"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Qiita APIからデータを取得できませんでした。")

        qiita_data = response.json()

    except httpx.ConnectError as e:
        logging.error(f"Qiita API通信エラーが発生しました。詳細: {e}")
        raise HTTPException(status_code=503, detail="Qiita APIへの接続に失敗しました。")
    except Exception as e:
        logging.error(f"予期せぬエラーが発生しました: {e}")
        raise HTTPException(status_code=500, detail="サーバー内部でエラーが発生しました。")

    clean_favorites = [{"title": item["title"], "url": item["url"]} for item in qiita_data]
    return clean_favorites

@router.post("/", response_model = ResponseSchema)
async def add_favorite(favorite: FavoriteSchema,
                       db: AsyncSession = Depends(db.get_db_session)):
    try:
        favorite.category = categorize_favorite(favorite.title)
        await favorite_crud.add_favorite(db, favorite)
        return ResponseSchema(message = "お気に入り登録しました")
    except Exception as e:
        raise HTTPException(status_code=400, detail="記事の登録に失敗しました。")

@router.get("/", response_model = list[FavoriteSchema])
async def get_favorite_list(db: AsyncSession = Depends(db.get_db_session)):
    favorites = await favorite_crud.list_favorite(db)
    return favorites

@router.delete("/{favorite_id}", response_model=ResponseSchema)
async def remove_favorite(favorite_id: int,
                          db: AsyncSession = Depends(db.get_db_session)):
    result = await favorite_crud.delete_favorite(db, favorite_id)
    if not result:
        raise HTTPException(status_code = 404, detail="削除対象が見つかりません")
    return ResponseSchema(message = "記事を削除しました")

def categorize_favorite(title: str) -> str:

    category = ai_model.categorize_ai(title)

    return category