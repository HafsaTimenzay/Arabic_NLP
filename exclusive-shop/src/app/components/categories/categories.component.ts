import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Category } from '../../models/product.model';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-categories',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './categories.component.html',
  styleUrl: './categories.component.scss'
})
export class CategoriesComponent implements OnInit {
  categories: Category[] = [];
constructor(private api: ApiService) {}

ngOnInit() {
  this.api.getCategories().subscribe((res: any) => {
    this.categories = res.map((c: any) => ({
      id: c.id,
      name: c.name,
      nameAr: c.name_ar,
      icon: c.icon,
      active: false
    }));
  });
}
  setActive(id: number) { this.categories = this.categories.map(c=>({...c,active:c.id===id})); }
}
