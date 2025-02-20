from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Table, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base

note_tag_association = Table(
    "Note_Tag",
    Base.metadata,
    Column("note_id", String(36), ForeignKey("Note.id")),
    Column("tag_id", String(36), ForeignKey("Tag.id")),
)


class Note(Base):
    __tablename__ = "Note"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), nullable=False, index=True)
    title = Column(String(64), nullable=False)
    content = Column(Text, nullable=False)
    memo_date = Column(String(8), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    """
    relationship 을 이용해서 다대다 관계를 설정
    back_populates 를 이용해서 태그를 가져올 때 관련된 노트를 가져올 수 있다.
    """
    tags = relationship("Tag", secondary=note_tag_association, back_populates="notes")


class Tag(Base):
    __tablename__ = "Tag"

    id = Column(String(36), primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    notes = relationship("Note", secondary=note_tag_association, back_populates="tags")
