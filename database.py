from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import asyncio
# Создаем базовый класс для объявления моделей
Base = declarative_base()

# Определяем модель для логирования API вызовов
class APILog(Base):
    __tablename__ = 'api_logs'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    rtsp_url = Column(String)
    user_info = Column(String)

# Создаем соединение с базой данных
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/fast_test"
engine = create_async_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем таблицы, если они еще не существуют
Base.metadata.create_all(bind=engine)

# Функция для добавления записи в лог API
def log_api_call(rtsp_url, user_info):
    db = SessionLocal()
    api_log = APILog(rtsp_url=rtsp_url, user_info=user_info)
    db.add(api_log)
    db.commit()
    db.close()