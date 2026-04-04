import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./pages/home/home.component').then(m => m.HomeComponent)
  },
  {
    path: 'product/:id',
    loadComponent: () => import('./pages/product-detail/product-detail.component').then(m => m.ProductDetailComponent)
  },
  {
    path: 'products',
    loadComponent: () => import('./components/explore-products/explore-products.component')
      .then(m => m.ExploreProductsComponent)
  },
  { 
    path: 'wishlist',
    loadComponent: () => import('./pages/wishlist/wishlist.component')
      .then(m => m.WishlistComponent)
  },
  { path: '**', redirectTo: '' }
];
