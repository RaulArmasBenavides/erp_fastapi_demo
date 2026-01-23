import datetime as dt
from sqlalchemy import Column, DateTime, Integer, Text

from app.infrastructure.repository.database import ORMBase
 
class EntrySchema(ORMBase):
    __tablename__ = "entries"  # nombre real de tabla (recomendado)

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=dt.datetime.utcnow, nullable=False)
