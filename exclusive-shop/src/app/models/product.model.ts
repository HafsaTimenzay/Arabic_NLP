export interface Product {
  id: number;
  name: string;
  nameAr: string;
  image: string;
  images?: string[];
  price: number;
  oldPrice?: number;
  discount?: number;
  rating: number;
  reviews: number;
  badge?: string;
  badgeType?: 'sale' | 'new';
  colors?: string[];
  sizes?: string[];
  category?: string;
  categoryAr?: string;
  description?: string;
  inStock?: boolean;
}

export interface Category {
  id: number;
  name: string;
  nameAr: string;
  icon: string;
  active?: boolean;
}

export interface Review {
  id: number;
  author: string;
  avatar?: string;
  initials?: string;
  avatarColor?: string;
  date: string;
  rating: number;
  text: string;
}
