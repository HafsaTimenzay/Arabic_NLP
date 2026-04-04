from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.wishlist import WishlistItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart_wishlist_review import WishlistOut

router = APIRouter(prefix="/wishlist", tags=["❤️ المفضلة"])


def _load(user_id: int, db: Session):
    return (
        db.query(WishlistItem)
        .options(joinedload(WishlistItem.product).joinedload(Product.category),
                 joinedload(WishlistItem.product).joinedload(Product.reviews))
        .filter(WishlistItem.user_id == user_id)
        .order_by(WishlistItem.created_at.desc())
        .all()
    )


@router.get("/", response_model=List[WishlistOut])
def get_wishlist(db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    return _load(current.id, db)


@router.post("/{product_id}", response_model=List[WishlistOut], status_code=201)
def add_to_wishlist(product_id: int, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()
    if not product:
        raise HTTPException(404, "المنتج غير موجود")
    exists = db.query(WishlistItem).filter(
        WishlistItem.user_id == current.id, WishlistItem.product_id == product_id
    ).first()
    if not exists:
        db.add(WishlistItem(user_id=current.id, product_id=product_id))
        db.commit()
    return _load(current.id, db)


@router.delete("/{product_id}", response_model=List[WishlistOut])
def remove_from_wishlist(product_id: int, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    item = db.query(WishlistItem).filter(
        WishlistItem.user_id == current.id, WishlistItem.product_id == product_id
    ).first()
    if item:
        db.delete(item)
        db.commit()
    return _load(current.id, db)


@router.delete("/", response_model=List[WishlistOut])
def clear_wishlist(db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    db.query(WishlistItem).filter(WishlistItem.user_id == current.id).delete()
    db.commit()
    return []
