import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ProductService } from '../../services/product.service';
import { Product } from '../../models/product.model';

@Component({ selector:'app-best-selling', standalone:true, imports:[CommonModule,RouterLink], templateUrl:'./best-selling.component.html', styleUrl:'./best-selling.component.scss' })
export class BestSellingComponent implements OnInit {
  products: Product[] = [];
  constructor(private ps: ProductService) {}
  ngOnInit() { this.products = this.ps.getBestSellingProducts(); }
  getStars(r:number){return Array(Math.floor(r)).fill(0);}
}
