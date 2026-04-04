from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id:         Mapped[int]      = mapped_column(primary_key=True, index=True)
    name:       Mapped[str]      = mapped_column(String(120))
    email:      Mapped[str]      = mapped_column(String(255), unique=True, index=True)
    password:   Mapped[str]      = mapped_column(String(255))
    phone:      Mapped[str|None] = mapped_column(String(30), nullable=True)
    avatar:     Mapped[str|None] = mapped_column(String(500), nullable=True)
    address:    Mapped[str|None] = mapped_column(Text, nullable=True)
    is_active:  Mapped[bool]     = mapped_column(Boolean, default=True)
    is_admin:   Mapped[bool]     = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    cart_items: Mapped[list["CartItem"]]     = relationship("CartItem",     back_populates="user", cascade="all, delete-orphan")  # noqa
    wishlist:   Mapped[list["WishlistItem"]] = relationship("WishlistItem", back_populates="user", cascade="all, delete-orphan")  # noqa
    orders:     Mapped[list["Order"]]        = relationship("Order",        back_populates="user")  # noqa
    reviews:    Mapped[list["Review"]]       = relationship("Review",       back_populates="user")  # noqa
