from sqlalchemy import Column, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String(50), unique=True, nullable=False, index=True)
    username = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=True)

    saved_designs = relationship("SavedDesign", back_populates="user", cascade="all, delete-orphan")


class NailDesign(Base):
    __tablename__ = "nail_designs"

    id = Column(Integer, primary_key=True, index=True)
    image_filename = Column(String(255), nullable=False, unique=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    tags = Column(String(255), nullable=False)

    saves = relationship("SavedDesign", back_populates="design", cascade="all, delete-orphan")

    @property
    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]


class SavedDesign(Base):
    __tablename__ = "saved_designs"
    __table_args__ = (UniqueConstraint("user_id", "design_id", name="uq_user_design"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    design_id = Column(Integer, ForeignKey("nail_designs.id"), nullable=False)

    user = relationship("User", back_populates="saved_designs")
    design = relationship("NailDesign", back_populates="saves")
