import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProductService } from '../../services/product.service';
import { Category } from '../../models/product.model';

@Component({
  selector: 'app-categories',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './categories.component.html',
  styleUrl: './categories.component.scss'
})
export class CategoriesComponent implements OnInit {
  categories: Category[] = [];
  constructor(private ps: ProductService) {}
  ngOnInit() { this.categories = this.ps.getCategories(); }
  setActive(id: number) { this.categories = this.categories.map(c=>({...c,active:c.id===id})); }
}
