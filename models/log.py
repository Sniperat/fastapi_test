from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class APILog(Base):
    __tablename__ = 'api_logs'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    rtsp_url = Column(String)
    user_info = Column(String)


Base.metadata.create_all(bind=engine)
