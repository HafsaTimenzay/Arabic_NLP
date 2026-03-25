import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.scss'
})
export class SidebarComponent {
  categories = [
    { label: 'أزياء المرأة',    hasArrow: true },
    { label: 'أزياء الرجل',     hasArrow: true },
    { label: 'الإلكترونيات',    hasArrow: true },
    { label: 'المنزل ونمط الحياة', hasArrow: false },
    { label: 'الأدوية',          hasArrow: false },
    { label: 'الرياضة والخارج', hasArrow: false },
    { label: 'الأطفال والألعاب', hasArrow: false },
    { label: 'البقالة والحيوانات', hasArrow: false },
    { label: 'الصحة والجمال',   hasArrow: false },
  ];
}
