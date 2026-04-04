import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { Product } from '../../models/product.model';
import { HeaderComponent } from '../../components/header/header.component';
import { FooterComponent } from '../../components/footer/footer.component';
import { ApiService } from 'src/app/services/api.service';

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

  constructor(private readonly api: ApiService) {}

  ngOnInit() {
    this.loadWishlist();
  }
 loadWishlist() {
  this.api.getWishlist().subscribe((res: any) => {

    this.wishlistItems = res.map((p: any) => ({
      id: p.id,
      name: p.name,
      nameAr: p.name_ar,
      image: p.image,
      price: p.price,
      oldPrice: p.old_price,
      badge: p.badge,
      badgeType: p.badge_type,
      rating: 4,
      reviews: 20
    }));

  });
}

 removeFromWishlist(id: number) {
  this.api.removeFromWishlist(id).subscribe(() => {
    this.loadWishlist(); // refresh
  });
}
  moveAllToBag() {
    alert(`تم نقل ${this.wishlistItems.length} منتجات إلى السلة!`);
  }

  }
