# 🛍️ Exclusive Shop — Backend API

واجهة برمجية REST API متكاملة للمتجر الإلكتروني Exclusive
**FastAPI + SQLAlchemy + SQLite + JWT**

---

## ⚡ تشغيل سريع

```bash
pip install -r requirements.txt
python -m app.services.seed        # قاعدة البيانات + بيانات أولية
uvicorn app.main:app --reload --port 8000
```

| رابط | الوصف |
|------|-------|
| http://localhost:8000/docs  | Swagger UI التفاعلي |
| http://localhost:8000/redoc | ReDoc documentation |

---

## 🔑 بيانات الدخول

| الدور | البريد | كلمة المرور |
|-------|--------|-------------|
| مشرف  | admin@exclusive.com | Admin@123  |
| مستخدم| user@exclusive.com  | User@1234  |

---

## 🐳 Docker

```bash
docker-compose up --build
```

---

## 📁 هيكل المشروع

```
exclusive-backend/
├── app/
│   ├── main.py                ← FastAPI app + CORS + routers
│   ├── core/
│   │   ├── config.py          ← إعدادات (.env)
│   │   ├── database.py        ← SQLAlchemy engine
│   │   ├── security.py        ← JWT + bcrypt
│   │   └── deps.py            ← get_current_user / get_current_admin
│   ├── models/                ← ORM tables
│   │   ├── user.py            ← User
│   │   ├── category.py        ← Category
│   │   ├── product.py         ← Product (soft-delete, avg_rating property)
│   │   ├── review.py          ← Review
│   │   ├── cart.py            ← CartItem
│   │   ├── wishlist.py        ← WishlistItem (unique constraint)
│   │   └── order.py           ← Order + OrderItem + OrderStatus enum
│   ├── schemas/               ← Pydantic v2 schemas
│   │   ├── user.py
│   │   ├── auth.py
│   │   ├── product.py         ← ProductOut, ProductListOut, CategoryOut
│   │   ├── cart_wishlist_review.py
│   │   └── order.py
│   ├── routers/               ← API endpoints
│   │   ├── auth.py            ← register / login / refresh / me
│   │   ├── users.py           ← profile / change-password
│   │   ├── categories.py      ← CRUD (create needs admin)
│   │   ├── products.py        ← list / get / CRUD + reviews
│   │   ├── cart.py            ← add / update / remove / clear
│   │   ├── wishlist.py        ← add / remove / clear
│   │   ├── orders.py          ← checkout / list / cancel / admin status
│   │   └── uploads.py         ← image upload + serve
│   └── services/
│       └── seed.py            ← 10 categories + 16 products + 2 users
├── angular-integration/
│   ├── api.service.ts         ← Angular HTTP service (نسخه إلى Angular)
│   └── auth.interceptor.ts    ← JWT interceptor
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

---

## 🛣️ API Endpoints

### Auth `/api/v1/auth`
```
POST /register       إنشاء حساب
POST /login          تسجيل دخول (OAuth2 form)
POST /refresh        تجديد token
GET  /me             بيانات المستخدم الحالي
```

### Products `/api/v1/products`
```
GET  /               قائمة (بحث + فلتر + صفحات)
GET  /flash-sales    تخفيضات سريعة
GET  /featured       منتجات مميزة
GET  /best-selling   الأكثر مبيعاً
GET  /related/{id}   منتجات ذات صلة
GET  /{id}           تفاصيل منتج
POST /               إنشاء [admin]
PATCH /{id}          تعديل [admin]
DELETE /{id}         حذف ناعم [admin]
GET  /{id}/reviews   التقييمات
POST /{id}/reviews   إضافة تقييم [auth]
```

### Cart `/api/v1/cart` [auth]
```
GET    /         جلب السلة
POST   /         إضافة منتج
PATCH  /{id}     تعديل كمية
DELETE /{id}     حذف عنصر
DELETE /         تفريغ السلة
```

### Wishlist `/api/v1/wishlist` [auth]
```
GET    /              جلب المفضلة
POST   /{product_id}  إضافة
DELETE /{product_id}  حذف
DELETE /              تفريغ
```

### Orders `/api/v1/orders` [auth]
```
POST /checkout        إتمام الشراء (يفرغ السلة)
GET  /                طلباتي
GET  /all             كل الطلبات [admin]
GET  /{id}            تفاصيل طلب
PATCH /{id}/status    تحديث الحالة [admin]
POST /{id}/cancel     إلغاء
```

### Categories `/api/v1/categories`
```
GET    /        كل الفئات
GET    /{slug}  فئة واحدة
POST   /        إنشاء [admin]
DELETE /{id}    حذف [admin]
```

### Uploads `/api/v1/uploads` [admin]
```
POST /{image}      رفع صورة
GET  /{filename}   عرض صورة
```

---

## 🔗 ربط Angular

```bash
# 1. انسخ ملفات التكامل
cp angular-integration/api.service.ts       exclusive-shop/src/app/services/
cp angular-integration/auth.interceptor.ts  exclusive-shop/src/app/core/
```

```typescript
// app.config.ts
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { authInterceptor } from './core/auth.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideAnimations(),
    provideHttpClient(withInterceptors([authInterceptor])),
  ]
};
```

```typescript
// مثال في أي Component
constructor(private api: ApiService) {}

ngOnInit() {
  // جلب التخفيضات السريعة من الـ API الحقيقي
  this.api.getFlashSales(4).subscribe(p => this.products = p);
}

addToCart(id: number) {
  this.api.addToCart(id, 1).subscribe(cart => {
    console.log(`السلة: ${cart.item_count} منتج`);
  });
}
```

---

## ⚙️ متغيرات البيئة (.env)

```env
DATABASE_URL=sqlite:///./exclusive.db
SECRET_KEY=change-this-to-a-strong-secret
ALLOWED_ORIGINS=http://localhost:4200
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
```

للانتقال لـ PostgreSQL:
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/exclusive_db
```
