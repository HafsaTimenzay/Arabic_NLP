import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from '../../components/header/header.component';
import { HeroBannerComponent } from '../../components/hero-banner/hero-banner.component';
import { FlashSalesComponent } from '../../components/flash-sales/flash-sales.component';
import { CategoriesComponent } from '../../components/categories/categories.component';
import { BestSellingComponent } from '../../components/best-selling/best-selling.component';
import { MusicBannerComponent } from '../../components/music-banner/music-banner.component';
import { ExploreProductsComponent } from '../../components/explore-products/explore-products.component';
import { NewArrivalComponent } from '../../components/new-arrival/new-arrival.component';
import { FooterComponent } from '../../components/footer/footer.component';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    HeaderComponent, HeroBannerComponent,
    FlashSalesComponent, CategoriesComponent, BestSellingComponent,
    MusicBannerComponent, ExploreProductsComponent, NewArrivalComponent,
    FooterComponent,
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {
  scrollTop() { window.scrollTo({ top: 0, behavior: 'smooth' }); }
  products: any;

  constructor(private readonly api: ApiService) { }

loadProducts() {
  this.api.getProducts().subscribe((res: any) => { // ← هنا نبدلنا النوع
    this.products = res.items.map((p: any) => ({
      id: p.id,
      name: p.name,
      nameAr: p.name_ar,
      image: p.image,
      price: p.price,
      oldPrice: p.old_price,
      categoryId: p.category_id,
      badge: p.badge,
      colors: p.colors,
      images: p.images
    }));
  });
}

}
