from sqlalchemy import Column, Integer, String, DateTime
from db import Base
from datetime import datetime

class Favorite(Base):
    __tablename__ = "favorite"

    id = Column(Integer, primary_key = True, autoincrement = True)

    title = Column(String(500))

    url = Column(String, unique = True)

    regist_date = Column(DateTime, default = datetime.now())

    category = Column(String(100), default = "未分類")