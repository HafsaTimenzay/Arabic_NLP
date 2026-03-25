import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ProductService } from '../../services/product.service';
import { Product } from '../../models/product.model';

@Component({ selector:'app-explore-products', standalone:true, imports:[CommonModule,RouterLink], templateUrl:'./explore-products.component.html', styleUrl:'./explore-products.component.scss' })
export class ExploreProductsComponent implements OnInit {
  products: Product[] = [];
  constructor(private ps: ProductService) {}
  ngOnInit() { this.products = this.ps.getExploreProducts(); }
  getStars(r:number){return Array(Math.floor(r)).fill(0);}
}
