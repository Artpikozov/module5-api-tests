from sqlalchemy import Column, Integer, String, Float, ForeignKey
from src.main.api.db.base import Base

class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    number = Column(String, unique=True,nullable=False )
    balance = Column(Float, nullable=False)

    def __repr__(self):  # этот метод нужен для удобного отображения объекта
        return f"<Account(id={self.id}, username={self.user_id}, role={self.number}, deleted_at={self.balance})>"