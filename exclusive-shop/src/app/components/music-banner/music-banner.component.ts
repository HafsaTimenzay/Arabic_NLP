import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-music-banner',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './music-banner.component.html',
  styleUrl: './music-banner.component.scss'
})
export class MusicBannerComponent implements OnInit, OnDestroy {
  hours = 5; minutes = 59; seconds = 35;
  private timer: any;
  ngOnInit() {
    this.timer = setInterval(() => {
      if (this.seconds > 0) this.seconds--;
      else if (this.minutes > 0) { this.minutes--; this.seconds = 59; }
      else if (this.hours > 0) { this.hours--; this.minutes = 59; this.seconds = 59; }
    }, 1000);
  }
  ngOnDestroy() { clearInterval(this.timer); }
  pad(n: number) { return n < 10 ? '0' + n : '' + n; }
}
