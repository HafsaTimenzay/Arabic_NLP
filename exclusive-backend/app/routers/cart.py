from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.cart import CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.cart_wishlist_review import CartItemCreate, CartItemUpdate, CartItemOut, CartOut

router = APIRouter(prefix="/cart", tags=["🛒 السلة"])


def _enrich(item: CartItem) -> CartItemOut:
    return CartItemOut(
        id=item.id,
        quantity=item.quantity,
        color=item.color,
        size=item.size,
        product=item.product,
        subtotal=round(item.product.price * item.quantity, 2),
        created_at=item.created_at,
    )


def _get_cart(user_id: int, db: Session):
    return (
        db.query(CartItem)
        .options(joinedload(CartItem.product).joinedload(Product.category),
                 joinedload(CartItem.product).joinedload(Product.reviews))
        .filter(CartItem.user_id == user_id)
        .all()
    )


@router.get("/", response_model=CartOut)
def get_cart(db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    items = _get_cart(current.id, db)
    enriched = [_enrich(i) for i in items]
    return CartOut(
        items=enriched,
        total=round(sum(i.subtotal for i in enriched), 2),
        item_count=sum(i.quantity for i in enriched),
    )


@router.post("/", response_model=CartOut, status_code=201)
def add_to_cart(payload: CartItemCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == payload.product_id, Product.is_active == True).first()
    if not product:
        raise HTTPException(404, "المنتج غير موجود")
    if product.stock < payload.quantity:
        raise HTTPException(400, f"الكمية المتاحة فقط {product.stock}")

    existing = db.query(CartItem).filter(
        CartItem.user_id == current.id,
        CartItem.product_id == payload.product_id,
        CartItem.color == payload.color,
        CartItem.size == payload.size,
    ).first()

    if existing:
        existing.quantity += payload.quantity
    else:
        item = CartItem(user_id=current.id, **payload.model_dump())
        db.add(item)

    db.commit()
    return get_cart(db=db, current=current)


@router.patch("/{item_id}", response_model=CartOut)
def update_cart_item(item_id: int, payload: CartItemUpdate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == current.id).first()
    if not item:
        raise HTTPException(404, "العنصر غير موجود في السلة")
    item.quantity = payload.quantity
    db.commit()
    return get_cart(db=db, current=current)


@router.delete("/{item_id}", response_model=CartOut)
def remove_cart_item(item_id: int, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == current.id).first()
    if not item:
        raise HTTPException(404, "العنصر غير موجود في السلة")
    db.delete(item)
    db.commit()
    return get_cart(db=db, current=current)


@router.delete("/", response_model=CartOut)
def clear_cart(db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    db.query(CartItem).filter(CartItem.user_id == current.id).delete()
    db.commit()
    return CartOut(items=[], total=0.0, item_count=0)
