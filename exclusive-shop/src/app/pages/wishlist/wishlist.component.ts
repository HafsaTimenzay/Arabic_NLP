import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ProductService } from '../../services/product.service';
import { Product } from '../../models/product.model';
import { HeaderComponent } from '../../components/header/header.component';
import { FooterComponent } from '../../components/footer/footer.component';

@Component({
  selector: 'app-wishlist',
  standalone: true,
  imports: [CommonModule, RouterLink, HeaderComponent, FooterComponent],
  templateUrl: './wishlist.component.html',
  styleUrl: './wishlist.component.scss'
})
export class WishlistComponent implements OnInit {
  wishlistItems: Product[] = [];
  recommendedItems: Product[] = [];

  constructor(private ps: ProductService) {}

  ngOnInit() {
    this.wishlistItems   = this.ps.getWishlistProducts();
    this.recommendedItems = this.ps.getJustForYouProducts();
  }

  removeFromWishlist(id: number) {
    this.wishlistItems = this.wishlistItems.filter(p => p.id !== id);
  }

  moveAllToBag() {
    alert(`تم نقل ${this.wishlistItems.length} منتجات إلى السلة!`);
  }

  getStars(r: number)      { return Array(Math.floor(r)).fill(0); }
  getEmptyStars(r: number) { return Array(5 - Math.floor(r)).fill(0); }
}
