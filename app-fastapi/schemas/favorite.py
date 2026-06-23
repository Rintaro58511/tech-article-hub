from pydantic import BaseModel, Field
from datetime import datetime

class FavoriteSchema(BaseModel):
    id: int | None = Field(default = None, description = "ここにお気に入り登録された記事のIDが入ります")

    title: str = Field(...,
                       description = "ここにお気に入り登録された記事のタイトルが入ります",
                       example = "pythonノック100本")
    
    url: str = Field(..., description = "ここにお気に入り登録された記事のURLが入ります")

    regist_date: datetime = Field(default = datetime.now())

    category: str = Field(..., description = "機械学習によって分類されたカテゴリ名が入ります")

class ResponseSchema(BaseModel):
    message: str = Field(...,
                         description = "API操作の結果を説明するメッセージ。",
                         example = "お気に入り追加できました。")