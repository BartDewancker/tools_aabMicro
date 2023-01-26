from database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship


class VideoTable(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True)
    path = Column(String(255))
    category_id = Column(Integer, ForeignKey("categories.id"))
    library_id = Column(Integer, ForeignKey("libraries.id"))
    annotation = Column(Text)
    category = relationship("CategoryTable", back_populates="videos", primaryjoin="VideoTable.category_id==CategoryTable.id")
    library = relationship("LibraryTable", back_populates="videos", primaryjoin="VideoTable.library_id==LibraryTable.id")


class CategoryTable(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    description = Column(String(100))
    videos = relationship("VideoTable", back_populates="category")

class LibraryTable(Base):
    __tablename__ = 'libraries'

    id = Column(Integer, primary_key=True)
    description = Column(String(50))
    videos = relationship("VideoTable", back_populates="library")