import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { Product } from '../../models/product.model';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-flash-sales',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './flash-sales.component.html',
  styleUrl: './flash-sales.component.scss'
})
export class FlashSalesComponent implements OnInit, OnDestroy {
  products: Product[] = [];
  days=3; hours=23; minutes=19; seconds=56;
  private timer: any;
 constructor(private api: ApiService) {}

ngOnInit() {
  this.loadProducts();
  this.timer = setInterval(() => this.tick(), 1000);
}

loadProducts() {
  this.api.getFlashSaleProducts().subscribe((res: any) => {

    this.products = res.map((p: any) => ({
      id: p.id,
      name: p.name,
      nameAr: p.name_ar,
      image: p.image,
      price: p.price,
      oldPrice: p.old_price,
      badge: p.badge,
      rating: p.avg_rating || 4 // 👈 زوين
    }));

  });
}
  ngOnDestroy() { clearInterval(this.timer); }
  tick() {
    if(this.seconds>0){this.seconds--;}
    else if(this.minutes>0){this.minutes--;this.seconds=59;}
    else if(this.hours>0){this.hours--;this.minutes=59;this.seconds=59;}
    else if(this.days>0){this.days--;this.hours=23;this.minutes=59;this.seconds=59;}
  }
  pad(n:number){return n<10?'0'+n:''+n;}
}
