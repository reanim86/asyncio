from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import Integer, String, Column

PG_DSN = 'postgresql+asyncpg://postgres:Tehn89tehn@127.0.0.1:5431/async'
engine = create_async_engine(PG_DSN)
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class SwapiPeople(Base):
    __tablename__ = 'swapipeople'

    id = Column(Integer, primary_key=True)
    birth_year = Column(String(length=15))
    eye_color = Column(String(length=20))
    films = Column(String)
    gender = Column(String(length=15))
    hair_color = Column(String(length=20))
    height = Column(String(length=15))
    homeworld = Column(String)
    mass = Column(Integer)
    name = Column(String(length=40))
    skin_color = Column(String(length=20))
    species = Column(String)
    starships = Column(String)
    vehicles = Column(String)

