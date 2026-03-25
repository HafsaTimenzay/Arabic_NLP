import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent }          from '../../components/header/header.component';
import { SidebarComponent }         from '../../components/sidebar/sidebar.component';
import { HeroBannerComponent }      from '../../components/hero-banner/hero-banner.component';
import { FlashSalesComponent }      from '../../components/flash-sales/flash-sales.component';
import { CategoriesComponent }      from '../../components/categories/categories.component';
import { BestSellingComponent }     from '../../components/best-selling/best-selling.component';
import { MusicBannerComponent }     from '../../components/music-banner/music-banner.component';
import { ExploreProductsComponent } from '../../components/explore-products/explore-products.component';
import { NewArrivalComponent }      from '../../components/new-arrival/new-arrival.component';
import { FooterComponent }          from '../../components/footer/footer.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    HeaderComponent, SidebarComponent, HeroBannerComponent,
    FlashSalesComponent, CategoriesComponent, BestSellingComponent,
    MusicBannerComponent, ExploreProductsComponent, NewArrivalComponent,
    FooterComponent,
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {
  scrollTop() { window.scrollTo({ top: 0, behavior: 'smooth' }); }
}
