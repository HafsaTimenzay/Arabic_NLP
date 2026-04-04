from datetime import datetime, timezone
from sqlalchemy import String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Review(Base):
    __tablename__ = "reviews"

    id:         Mapped[int]      = mapped_column(primary_key=True, index=True)
    rating:     Mapped[int]      = mapped_column(Integer, nullable=False)   # 1-5
    title:      Mapped[str|None] = mapped_column(String(200), nullable=True)
    body:       Mapped[str]      = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user_id:    Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))

    user:    Mapped["User"]    = relationship("User",    back_populates="reviews")   # noqa
    product: Mapped["Product"] = relationship("Product", back_populates="reviews")  # noqa
