import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';

@Component({ selector:'app-footer', standalone:true, imports:[CommonModule,FormsModule,RouterLink], templateUrl:'./footer.component.html', styleUrl:'./footer.component.scss' })
export class FooterComponent {
  email = '';
  currentYear = new Date().getFullYear();
  quickLinks   = ['سياسة الخصوصية','شروط الاستخدام','الأسئلة الشائعة','تواصل معنا'];
  accountLinks = ['حسابي','تسجيل الدخول / إنشاء حساب','السلة','المفضلة','المتجر'];
  supportLinks = ['١١١ بيجوي سراني، دكا، بنغلاديش.','exclusive@gmail.com','+88015-88888-9999'];
  subscribe() { if(this.email){alert('تم الاشتراك بنجاح!');this.email='';} }
}
