import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from 'src/app/services/api.service';
import { Product } from '../../models/product.model';

@Component({ selector:'app-best-selling', standalone:true, imports:[CommonModule,RouterLink], templateUrl:'./best-selling.component.html', styleUrl:'./best-selling.component.scss' })
export class BestSellingComponent implements OnInit {

  products: any[] = [];
  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadProducts();
  }
  loadProducts() {
    this.api.getProducts().subscribe((res: any) => {

      this.products = res.items
        .filter((p: any) => p.is_featured)
        .map((p: any) => ({
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
