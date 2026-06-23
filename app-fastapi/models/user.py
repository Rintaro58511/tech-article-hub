from sqlalchemy import Column, Integer, String, DateTime
from db import Base
from pwdlib import PasswordHash

class User(Base):
    __tablename__ = "user"

    password_hash = PasswordHash.recommended()

    id = Column(Integer, primary_key = True, autoincrement = True)

    user_name = Column(String(50), nullable = False, unique = True)

    password = Column(String(255), nullable = False)

    def set_password(self, password):
        self.password = self.password_hash.hash(password)
    
    def check_password(self, password):
        return self.password_hash.verify(password, self.password)