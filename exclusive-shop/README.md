# Exclusive — متجر إلكتروني بالعربية (Angular 17)

تطبيق Angular 17 كامل لمتجر إلكتروني باللغة العربية مع دعم RTL.

## 🚀 تشغيل المشروع

```bash
npm install
ng serve
# http://localhost:4200
```

## 📄 الصفحات

| المسار | الصفحة |
|--------|--------|
| `/` | الصفحة الرئيسية |
| `/product/:id` | تفاصيل المنتج |
| `/wishlist` | المفضلة |

## 📁 هيكل المشروع

```
src/app/
├── pages/
│   ├── home/               ← الصفحة الرئيسية
│   ├── product-detail/     ← تفاصيل المنتج + مراجعات + منتجات ذات صلة
│   └── wishlist/           ← المفضلة + فقط لك
├── components/
│   ├── header/             ← شريط الإعلانات + التنقل
│   ├── sidebar/            ← قائمة الفئات
│   ├── hero-banner/        ← بانر تلقائي
│   ├── flash-sales/        ← عداد تنازلي + منتجات
│   ├── categories/         ← تصفح الفئات
│   ├── best-selling/       ← الأكثر مبيعاً
│   ├── music-banner/       ← بانر ترويجي
│   ├── explore-products/   ← استكشف المنتجات
│   ├── new-arrival/        ← وصل حديثاً
│   └── footer/             ← تذييل الصفحة
├── models/product.model.ts ← نماذج البيانات
└── services/product.service.ts ← بيانات المنتجات
```

## ✨ المميزات

- **RTL كامل** — Arabic right-to-left layout
- **خط Cairo/Tajawal** — خطوط عربية احترافية
- **Angular 17** standalone components بدون NgModules
- **Lazy loading** للصفحات
- **عدادات تنازلية** حية
- **صفحة تفاصيل المنتج** مع معرض صور وتقييمات
- **صفحة المفضلة** مع إضافة/حذف
- **تصميم متجاوب** (Responsive)
