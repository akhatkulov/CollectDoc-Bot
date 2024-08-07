from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, BigInteger, func,VARCHAR,desc
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from conf import DB_URL

engine = create_engine(DB_URL, echo=True, future=True)


Base = declarative_base()

user_table_name = 'user_collect'
user_info_table_name = 'user_info_collect'
channels_table_name = 'channels_collect'


class User(Base):
    __tablename__ = user_table_name
    id = Column(Integer, primary_key=True, autoincrement=True)
    cid = Column(BigInteger, unique=True)
    step = Column(String, default="0")

class User_Info(Base):
    __tablename__ = user_info_table_name
    id = Column(Integer, primary_key=True, autoincrement=True)
    cid = Column(String, unique=True)
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



def get_all_user():
    try:
        x = session.query(User.cid).all()
        res = [i[0] for i in x]
        return res
    finally:
        session.close()

def user_count():
    try:
        x = session.query(func.count(User.id)).first()
        return x[0]
    finally:
        session.close()

def create_user(cid,name):
    try:
        user = User(cid=int(cid), step="0", ball=0,name=name,phone="*")
        session.add(user)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

def get_members():
    try:
        x = session.query(User).where(User.cid >= 0).all()
        return x
    finally:
        session.close()

# Function to get the step for a given CID
def get_step(cid):
    try:
        x = session.query(User).filter_by(cid=cid).first()
        return x.step if x else None
    finally:
        session.close()

def put_step(cid, step):
    try:
        x = session.query(User).filter_by(cid=cid).first()
        if x:
            x.step = str(step)
            session.commit()
            return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error: {e}")
        return False

def put_channel(channel: str):
    try:
        x = Channels(link=channel)
        session.add(x)
        session.commit()
        return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error: {e}")
        return False

def get_channel():
    try:
        x = session.query(Channels).all()
        res = [i.link for i in x]
        return res
    finally:
        session.close()

def get_channel_with_id():
    try:
        x = session.query(Channels).all()
        res = ""
        for channel in x:
            res += f"\nID: {channel.id} \nLink: @{channel.link}"
        return res
    finally:
        session.close()

def delete_channel(ch_id):
    try:
        x = session.query(Channels).filter_by(id=int(ch_id)).first()
        if x:
            session.delete(x)
            session.commit()
            return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error: {e}")
        return False



# Function to change user information
def change_info(cid : int, type_info : str, value : str):
    x = session.query(User_info).filter_by(cid=cid).first()
    try:
        info = session.query(User_info).filter_by(cid=cid).first()
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
            session.commit()
            return True
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error: {e}")
        return False
    finally:
        session.close()

# Function to get user information
def get_info(cid: int):
    try:
        x = session.query(User_Info).filter_by(cid=cid).first()
        if x:
            res = {
                "cid": cid,
                "person_type": x.person_type,
                "passport": x.passport_file_id,
                "diplom": x.diplom_id,
                "obyektiv": x.obyektiv_id,
                "lang": x.lang_id,
                "legal": x.legal_id
            }
            return res
        else:
            return None
    except SQLAlchemyError as e:
        print(f"Error: {e}")
    finally:
        session.close()

