import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';
import { Product, Review } from '../../models/product.model';
import { HeaderComponent } from '../../components/header/header.component';
import { FooterComponent } from '../../components/footer/footer.component';

@Component({
  selector: 'app-product-detail',
  standalone: true,
  imports: [CommonModule, RouterLink, HeaderComponent, FooterComponent],
  templateUrl: './product-detail.component.html',
  styleUrl: './product-detail.component.scss'
})
export class ProductDetailComponent implements OnInit {
  product?: Product;
  relatedProducts: Product[] = [];
  reviews: Review[] = [];
  selectedImage = 0;
  selectedColor = 0;
  selectedSize = 'M';
  quantity = 2;
  addedToWishlist = false;
  addedToCart = false;

  constructor(private route: ActivatedRoute, private api: ApiService) {}

ngOnInit() {
  this.route.params.subscribe(p => {
    const id = +p['id'];

    this.api.getProductById(id).subscribe(res => {

      this.product = {
        id: res.id,
        name: res.name,
        nameAr: res.name_ar,
        image: res.image,
        images: res.images,
        price: res.price,
        oldPrice: res.old_price,
        colors: res.colors,
        sizes: res.sizes,
        rating: res.rating ?? 0,
        reviews: res.reviews ?? []
      };

      this.selectedImage = 0;
      this.addedToCart = false;
      window.scrollTo(0, 0);

    });
  });
}

  setImage(i: number) { this.selectedImage = i; }

  getImages(): string[] {
    if (this.product?.images?.length) return this.product.images;
    const img = this.product?.image ?? '';
    return [img, img, img, img];
  }


  changeQty(delta: number) { this.quantity = Math.max(1, this.quantity + delta); }
  toggleWishlist()  { this.addedToWishlist = !this.addedToWishlist; }
  addToCart()       { this.addedToCart = true; setTimeout(() => this.addedToCart = false, 2000); }
}
