from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class BlackList(Base):
    __tablename__ = "black_lists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="black_list")

