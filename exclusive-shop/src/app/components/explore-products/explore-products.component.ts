import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { Product } from '../../models/product.model';
import { ApiService } from 'src/app/services/api.service';

@Component({ 
  selector:'app-explore-products', 
  standalone:true,
   imports:[CommonModule,RouterLink], 
   templateUrl:'./explore-products.component.html', 
   styleUrl:'./explore-products.component.scss'
 })
export class ExploreProductsComponent implements OnInit {
  products: Product[] = [];
 constructor(private api: ApiService) {}

ngOnInit() {
  this.api.getProducts().subscribe((res: any) => {

    this.products = res.items.map((p: any) => ({
      id: p.id,
      name: p.name,
      nameAr: p.name_ar,
      image: p.image,
      price: p.price,
      oldPrice: p.old_price,
      rating: 4
    }));

  });
}
}
