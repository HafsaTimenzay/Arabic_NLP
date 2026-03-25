import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-hero-banner',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './hero-banner.component.html',
  styleUrl: './hero-banner.component.scss'
})
export class HeroBannerComponent implements OnInit, OnDestroy {
  slides = [
    { brand: 'سلسلة iPhone 14', title: 'خصم يصل\nإلى 10%', image: 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&q=80' },
    { brand: 'سامسونج جالاكسي', title: 'أفضل العروض\nهذا الأسبوع', image: 'https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400&q=80' },
    { brand: 'MacBook Pro', title: 'القوة تلتقي\nبالأناقة', image: 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&q=80' },
  ];
  activeSlide = 0;
  private timer: any;

  ngOnInit() { this.timer = setInterval(() => this.next(), 4000); }
  ngOnDestroy() { clearInterval(this.timer); }
  next() { this.activeSlide = (this.activeSlide + 1) % this.slides.length; }
  setSlide(i: number) { this.activeSlide = i; clearInterval(this.timer); this.timer = setInterval(() => this.next(), 4000); }
}
