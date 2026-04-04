from sqlalchemy import String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Category(Base):
    __tablename__ = "categories"

    id:          Mapped[int]      = mapped_column(primary_key=True, index=True)
    name:        Mapped[str]      = mapped_column(String(100))
    name_ar:     Mapped[str]      = mapped_column(String(100))
    slug:        Mapped[str]      = mapped_column(String(120), unique=True, index=True)
    icon:        Mapped[str|None] = mapped_column(String(80), nullable=True)
    description: Mapped[str|None] = mapped_column(Text, nullable=True)
    is_active:   Mapped[bool]     = mapped_column(Boolean, default=True)

    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")  # noqa
