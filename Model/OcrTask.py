from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, func, update
from db import Db
from db import Base

class TaskState(Enum):
    NEW = 'NEW'
    PENDING = 'PENDING'
    DONE = 'DONE'

class OcrTaskModel(Base):
    __tablename__ = 'ocrTasks'
    id = Column('id', String(500), primary_key=True)
    status = Column('status', String(40))
    created = Column('created', DateTime, default=func.now())

    @classmethod
    def find_by_id(cls, task_id):
        session = Db.get_db_session()
        return session.query(cls).filter_by(id=task_id).first()

    @classmethod
    def delete_by_id(cls, task_id):
        session = Db.get_db_session()
        return session.query(cls).filter_by(id=task_id).delete()

    @classmethod
    def change_status(cls, task_id, task_status):
       session = Db.get_db_session()
       task = session.query(cls).filter_by(id=task_id).first()
       task.status = task_status
       session.commit()
        

