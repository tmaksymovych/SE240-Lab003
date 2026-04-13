from sqlalchemy import Column, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)

    skipasses = relationship("SkiPass", back_populates="visitor")

class SkiPass(Base):
    __tablename__ = "skipasses"

    id = Column(String, primary_key=True)
    visitor_id = Column(String, ForeignKey("visitor.id"))
    pass_type = Column(String, nullable=False)
    price = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    visitor = relationship("Visitor", back_populates="skipasses")



