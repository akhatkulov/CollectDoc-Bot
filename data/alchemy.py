import asyncio
from sqlalchemy import Column, Integer, String, BigInteger, func, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from conf import DB_URL



engine = create_async_engine(DB_URL, echo=True,future=True)

Base = declarative_base()

user_table_name = 'user_ball'
user_info_table_name = 'user_info_table_name'
channels_table_name = 'channels_ball'

class User(Base):
    __tablename__ = user_table_name
    id = Column(Integer, primary_key=True, autoincrement=True)
    cid = Column(BigInteger, unique=True)
    step = Column(VARCHAR(25), default=0)
    
class User_Info(Base):
    __tablename__ = user_info_table_name
    id = Column(Integer, primary_key=True, autoincrement=True)  # Added primary key
    cid = Column(BigInteger, unique=True)
    person_type = Column(String)
    passport_file_id = Column(String)
    diplom_id = Column(String)
    obyektiv_id = Column(String)
    lang_id = Column(String)
    legal_id = Column(String)
class Channels(Base):
    __tablename__ = channels_table_name
    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String, default="None", unique=True)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def get_all_user():
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(f'SELECT cid FROM {user_table_name}')
            res = [row.cid for row in result.fetchall()]
            return res
        except SQLAlchemyError as e:
            print(f"Error: {e}")

async def user_count():
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(f'SELECT COUNT(id) FROM {user_table_name}')
            return result.scalar()
        except SQLAlchemyError as e:
            print(f"Error: {e}")

async def create_user(cid, name):
    async with AsyncSessionLocal() as session:
        try:
            user = User(cid=int(cid), step="0")
            info = User_Info(cid=int(cid), person_type="None", passport_file_id="None", diplom_id="None", obyektiv_id="None", lang_id="None", legal_id="None")
            session.add(user)
            session.add(info)
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            print(f"Error: {e}")

async def get_members():
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(f'SELECT * FROM {user_table_name} WHERE cid >= 0')
            return result.scalars().all()
        except SQLAlchemyError as e:
            print(f"Error: {e}")

async def get_step(cid):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(f'SELECT step FROM {user_table_name} WHERE cid = :cid', {'cid': cid})
            row = result.fetchone()
            return row.step if row else None
        except SQLAlchemyError as e:
            print(f"Error: {e}")

async def put_step(cid, step):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(f'SELECT * FROM {user_table_name} WHERE cid = :cid', {'cid': cid})
            user = result.scalar_one_or_none()
            if user:
                user.step = str(step)
                await session.commit()
                return True
        except SQLAlchemyError as e:
            await session.rollback()
            print(f"Error: {e}")
        return False

async def put_channel(channel: str):
    async with AsyncSessionLocal() as session:
        try:
            ch = Channels(link=channel)
            session.add(ch)
            await session.commit()
            return True
        except SQLAlchemyError as e:
            await session.rollback()
            print(f"Error: {e}")
        return False

async def get_channel():
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(f'SELECT link FROM {channels_table_name}')
            return [row.link for row in result.fetchall()]
        except SQLAlchemyError as e:
            print(f"Error: {e}")

async def get_channel_with_id():
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(f'SELECT id, link FROM {channels_table_name}')
            channels = result.fetchall()
            return '\n'.join(f"ID: {ch.id} \nLink: @{ch.link}" for ch in channels)
        except SQLAlchemyError as e:
            print(f"Error: {e}")

async def delete_channel(ch_id):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(f'SELECT * FROM {channels_table_name} WHERE id = :id', {'id': ch_id})
            channel = result.scalar_one_or_none()
            if channel:
                await session.delete(channel)
                await session.commit()
                return True
        except SQLAlchemyError as e:
            await session.rollback()
            print(f"Error: {e}")
        return False

async def change_info(cid: int, type_info: str, value: str):
    async with AsyncSessionLocal() as session:
        try:
            x = await session.execute(f'SELECT * FROM {user_info_table_name} WHERE cid = :cid', {'cid': cid})
            info = x.scalar_one_or_none()
            if info:
                if type_info == "person_type":
                    info.person_type = value
                elif type_info == "passport_file_id":
                    info.passport_file_id = value
                elif type_info == "diplom_id":
                    info.diplom_id = value
                elif type_info == "obyektiv_id":
                    info.obyektiv_id = value
                elif type_info == "lang_id":
                    info.lang_id = value
                elif type_info == "legal_id":
                    info.legal_id = value
                await session.commit()
                return True
        except SQLAlchemyError as e:
            await session.rollback()
            print(f"Error: {e}")
        return False

async def main():
    await create_tables()

if __name__ == '__main__':
    asyncio.run(main())
