import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_user, get_current_admin
from app.models.order import Order, OrderItem, OrderStatus
from app.models.cart import CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate, OrderOut, OrderStatusUpdate

router = APIRouter(prefix="/orders", tags=["📋 الطلبات"])


def _load_order(order_id: int, db: Session) -> Order:
    order = (
        db.query(Order)
        .options(joinedload(Order.items).joinedload(OrderItem.product))
        .filter(Order.id == order_id)
        .first()
    )
    if not order:
        raise HTTPException(404, "الطلب غير موجود")
    return order


def _enrich_out(order: Order) -> OrderOut:
    items_out = []
    for i in order.items:
        items_out.append({
            "id": i.id,
            "quantity": i.quantity,
            "unit_price": i.unit_price,
            "color": i.color,
            "size": i.size,
            "product_id": i.product_id,
            "product_name": i.product.name_ar if i.product else None,
        })
    return OrderOut(
        id=order.id,
        order_number=order.order_number,
        status=order.status,
        status_ar=order.status_ar,
        total=order.total,
        shipping_cost=order.shipping_cost,
        discount=order.discount,
        shipping_address=order.shipping_address,
        notes=order.notes,
        items=items_out,
        created_at=order.created_at,
        updated_at=order.updated_at,
    )


@router.post("/checkout", response_model=OrderOut, status_code=201)
def checkout(payload: OrderCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    cart_items = (
        db.query(CartItem)
        .options(joinedload(CartItem.product))
        .filter(CartItem.user_id == current.id)
        .all()
    )
    if not cart_items:
        raise HTTPException(400, "السلة فارغة")

    # Validate stock
    for ci in cart_items:
        if not ci.product or not ci.product.is_active:
            raise HTTPException(400, f"المنتج {ci.product_id} غير متاح")
        if ci.product.stock < ci.quantity:
            raise HTTPException(400, f"الكمية المتاحة من {ci.product.name_ar} هي {ci.product.stock} فقط")

    subtotal = sum(ci.product.price * ci.quantity for ci in cart_items)
    shipping = 0.0 if subtotal >= 140 else 10.0
    total = subtotal + shipping

    order = Order(
        order_number=f"EX-{uuid.uuid4().hex[:8].upper()}",
        user_id=current.id,
        total=round(total, 2),
        shipping_cost=shipping,
        shipping_address=payload.shipping_address,
        notes=payload.notes,
    )
    db.add(order)
    db.flush()

    for ci in cart_items:
        db.add(OrderItem(
            order_id=order.id,
            product_id=ci.product_id,
            quantity=ci.quantity,
            unit_price=ci.product.price,
            color=ci.color,
            size=ci.size,
        ))
        ci.product.stock -= ci.quantity

    # Clear cart
    db.query(CartItem).filter(CartItem.user_id == current.id).delete()
    db.commit()

    return _enrich_out(_load_order(order.id, db))


@router.get("/", response_model=List[OrderOut])
def my_orders(db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    orders = (
        db.query(Order)
        .options(joinedload(Order.items).joinedload(OrderItem.product))
        .filter(Order.user_id == current.id)
        .order_by(Order.created_at.desc())
        .all()
    )
    return [_enrich_out(o) for o in orders]


@router.get("/all", response_model=List[OrderOut], dependencies=[Depends(get_current_admin)])
def all_orders(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    orders = (
        db.query(Order)
        .options(joinedload(Order.items).joinedload(OrderItem.product))
        .order_by(Order.created_at.desc())
        .offset(skip).limit(limit).all()
    )
    return [_enrich_out(o) for o in orders]


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    order = _load_order(order_id, db)
    if order.user_id != current.id and not current.is_admin:
        raise HTTPException(403, "غير مصرح")
    return _enrich_out(order)


@router.patch("/{order_id}/status", response_model=OrderOut, dependencies=[Depends(get_current_admin)])
def update_status(order_id: int, payload: OrderStatusUpdate, db: Session = Depends(get_db)):
    order = _load_order(order_id, db)
    order.status = payload.status
    db.commit()
    return _enrich_out(_load_order(order_id, db))


@router.post("/{order_id}/cancel", response_model=OrderOut)
def cancel_order(order_id: int, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    order = _load_order(order_id, db)
    if order.user_id != current.id and not current.is_admin:
        raise HTTPException(403, "غير مصرح")
    if order.status not in (OrderStatus.pending, OrderStatus.confirmed):
        raise HTTPException(400, "لا يمكن إلغاء الطلب في هذه المرحلة")
    order.status = OrderStatus.cancelled
    # Restore stock
    for item in order.items:
        if item.product:
            item.product.stock += item.quantity
    db.commit()
    return _enrich_out(_load_order(order_id, db))
