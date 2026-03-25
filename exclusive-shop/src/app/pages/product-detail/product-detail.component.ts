import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ProductService } from '../../services/product.service';
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

  constructor(private route: ActivatedRoute, private ps: ProductService) {}

  ngOnInit() {
    this.route.params.subscribe(p => {
      const id = +p['id'];
      this.product = this.ps.getProductById(id) ?? this.ps.getAllProducts()[0];
      this.selectedImage = 0;
      this.addedToCart = false;
      window.scrollTo(0, 0);
    });
    this.relatedProducts = this.ps.getRelatedProducts();
    this.reviews = this.ps.getReviews();
  }

  setImage(i: number) { this.selectedImage = i; }

  getImages(): string[] {
    if (this.product?.images?.length) return this.product.images;
    const img = this.product?.image ?? '';
    return [img, img, img, img];
  }

  getStars(r: number)      { return Array(Math.floor(r)).fill(0); }
  getEmptyStars(r: number) { return Array(5 - Math.floor(r)).fill(0); }

  changeQty(delta: number) { this.quantity = Math.max(1, this.quantity + delta); }
  toggleWishlist()  { this.addedToWishlist = !this.addedToWishlist; }
  addToCart()       { this.addedToCart = true; setTimeout(() => this.addedToCart = false, 2000); }
}
