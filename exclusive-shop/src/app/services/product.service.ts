// import { Injectable } from '@angular/core';
// import { Product, Category, Review } from '../models/product.model';

// @Injectable({ providedIn: 'root' })
// export class ProductService {

//   private allProducts: Product[] = [
//     { id: 1,  nameAr: 'ذراع تحكم HAVIT HV-G92',    name: 'HAVIT HV-G92 Gamepad',         image: 'https://images.unsplash.com/photo-1593508512255-86ab42a8e620?w=400&q=80', images: ['https://images.unsplash.com/photo-1593508512255-86ab42a8e620?w=600&q=80','https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?w=600&q=80','https://images.unsplash.com/photo-1585620385456-4759f9b5c7d9?w=600&q=80','https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=600&q=80'], price: 120, oldPrice: 160, discount: -40, rating: 4.5, reviews: 88, badge: '-40%', badgeType: 'sale', colors: ['#4493F8','#DB4444'], sizes: ['XS','S','M','L','XL'], category: 'Gaming', categoryAr: 'ألعاب', description: 'جهاز تحكم بلايستيشن 5 عالي الجودة مع لاصق هوائي للتثبيت السهل والإزالة الخالية من الفقاعات.' },
//     { id: 2,  nameAr: 'لوحة مفاتيح AK-900',         name: 'AK-900 Wired Keyboard',         image: 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&q=80', price: 960, oldPrice: 1160, discount: -35, rating: 4.5, reviews: 75, badge: '-35%', badgeType: 'sale', category: 'Electronics', categoryAr: 'إلكترونيات' },
//     { id: 3,  nameAr: 'شاشة ألعاب IPS LCD',         name: 'IPS LCD Gaming Monitor',        image: 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&q=80', price: 370, oldPrice: 400, discount: -30, rating: 4.5, reviews: 99, badge: '-30%', badgeType: 'sale', category: 'Electronics', categoryAr: 'إلكترونيات' },
//     { id: 4,  nameAr: 'كرسي S-Series مريح',          name: 'S-Series Comfort Chair',        image: 'https://images.unsplash.com/photo-1592078615290-033ee584e267?w=400&q=80', price: 375, oldPrice: 400, discount: -25, rating: 4.5, reviews: 99, badge: '-25%', badgeType: 'sale', category: 'Home', categoryAr: 'المنزل' },
//     { id: 5,  nameAr: 'معطف نورث فيس',               name: 'The North Coat',                image: 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400&q=80', price: 260, oldPrice: 360, rating: 5, reviews: 65, category: 'Fashion', categoryAr: 'أزياء' },
//     { id: 6,  nameAr: 'حقيبة غوتشي',                 name: 'Gucci Duffle Bag',              image: 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&q=80', price: 960, oldPrice: 1160, rating: 4.5, reviews: 65, category: 'Fashion', categoryAr: 'أزياء' },
//     { id: 7,  nameAr: 'مبرد CPU بالسائل RGB',        name: 'RGB Liquid CPU Cooler',         image: 'https://images.unsplash.com/photo-1587831990711-23ca6441447b?w=400&q=80', price: 160, oldPrice: 170, rating: 4.5, reviews: 65, category: 'Computers', categoryAr: 'حاسوب' },
//     { id: 8,  nameAr: 'رف كتب صغير',                  name: 'Small BookShelf',               image: 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&q=80', price: 360, rating: 5, reviews: 65, category: 'Home', categoryAr: 'المنزل' },
//     { id: 9,  nameAr: 'طعام جاف للكلاب',              name: 'Breed Dry Dog Food',            image: 'https://images.unsplash.com/photo-1589924691995-400dc9ecc119?w=400&q=80', price: 100, rating: 3, reviews: 35, category: 'Pets', categoryAr: 'الحيوانات' },
//     { id: 10, nameAr: 'كاميرا كانون DSLR',            name: 'CANON EOS DSLR Camera',        image: 'https://images.unsplash.com/photo-1606983340126-99ab4feaa64a?w=400&q=80', price: 360, rating: 4, reviews: 95, category: 'Electronics', categoryAr: 'إلكترونيات' },
//     { id: 11, nameAr: 'لابتوب ASUS للألعاب',          name: 'ASUS FHD Gaming Laptop',       image: 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=400&q=80', price: 700, oldPrice: 960, rating: 5, reviews: 325, badge: 'جديد', badgeType: 'new', category: 'Computers', categoryAr: 'حاسوب' },
//     { id: 12, nameAr: 'مجموعة منتجات التجميل',        name: 'Cosmology Product Set',        image: 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400&q=80', price: 197, rating: 4, reviews: 325, category: 'Beauty', categoryAr: 'جمال' },
//     { id: 13, nameAr: 'سيارة كهربائية للأطفال',       name: 'Kids Electric Car',            image: 'https://images.unsplash.com/photo-1594787318286-3d835c1d207f?w=400&q=80', price: 960, oldPrice: 1160, rating: 5, reviews: 65, badge: 'رائج', badgeType: 'new', colors: ['#E00000','#000000'], category: 'Toys', categoryAr: 'ألعاب أطفال' },
//     { id: 14, nameAr: 'حذاء كرة قدم Jr. Zoom',       name: 'Jr. Zoom Soccer Cleats',       image: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&q=80', price: 1160, oldPrice: 1360, rating: 4.5, reviews: 35, colors: ['#FFD700','#00CC00'], category: 'Sports', categoryAr: 'رياضة' },
//     { id: 15, nameAr: 'ذراع تحكم GP11 Shooter',      name: 'GP11 Shooter USB Gamepad',     image: 'https://images.unsplash.com/photo-1612287230202-1ff1d85d1bdf?w=400&q=80', price: 660, oldPrice: 1160, rating: 4.5, reviews: 55, badge: '-45%', badgeType: 'sale', colors: ['#000000','#333333'], category: 'Gaming', categoryAr: 'ألعاب' },
//     { id: 16, nameAr: 'جاكيت ساتان مبطن',            name: 'Quilted Satin Jacket',         image: 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&q=80', price: 660, rating: 4.5, reviews: 55, badge: 'جديد', badgeType: 'new', colors: ['#2F4F4F','#000000'], category: 'Fashion', categoryAr: 'أزياء' },
//   ];

//   getFlashSaleProducts(): Product[]   { return this.allProducts.slice(0, 4); }
//   getBestSellingProducts(): Product[] { return this.allProducts.slice(4, 8); }
//   getExploreProducts(): Product[]     { return this.allProducts.slice(8, 16); }
//   getRelatedProducts(): Product[]     { return this.allProducts.slice(0, 4); }
//   getWishlistProducts(): Product[]    { return [this.allProducts[5], this.allProducts[6], this.allProducts[14], this.allProducts[15]]; }
//   getJustForYouProducts(): Product[]  { return [this.allProducts[10], this.allProducts[2], this.allProducts[0], this.allProducts[1]]; }
//   getAllProducts(): Product[]         { return this.allProducts; }

//   getProductById(id: number): Product | undefined {
//     return this.allProducts.find(p => p.id === id);
//   }

//   getCategories(): Category[] {
//     return [
//       { id:1, name:'Phones',      nameAr:'الهواتف',     icon:'fa-mobile-alt' },
//       { id:2, name:'Computers',   nameAr:'الحاسوب',     icon:'fa-laptop' },
//       { id:3, name:'SmartWatch',  nameAr:'الساعات',     icon:'fa-clock' },
//       { id:4, name:'Camera',      nameAr:'الكاميرا',    icon:'fa-camera', active:true },
//       { id:5, name:'HeadPhones',  nameAr:'السماعات',    icon:'fa-headphones' },
//       { id:6, name:'Gaming',      nameAr:'الألعاب',     icon:'fa-gamepad' },
//     ];
//   }

//   getReviews(): Review[] {
//     return [
//       { id:1, author:'أحمد الشمري', initials:'أ', avatarColor:'#DB4444', date:'منذ شهر', rating:4, text:'منتج ممتاز جداً، وصل في الوقت المحدد والتغليف كان رائعاً. أنصح بالشراء منهم، سعر جيد مقابل الجودة العالية.' },
//       { id:2, author:'سارة المنصور', initials:'س', avatarColor:'#4493F8', date:'منذ 6 أيام', rating:4, text:'كتبت مراجعتي بعد 4 أشهر من الاستخدام. كانت هناك بعض الأخطاء الصغيرة في البداية ولكن تم حلها بسرعة. الجودة ممتازة ونوصي باستمرار التعامل معهم.' },
//     ];
//   }
// }
