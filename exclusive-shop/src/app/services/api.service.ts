import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private readonly baseUrl = 'http://127.0.0.1:8000';

  constructor(private readonly http: HttpClient) { }

  getProducts() {
    return this.http.get<any[]>(`${this.baseUrl}/api/v1/products`);
  }
  getProductById(id: number) {
    return this.http.get<any>(`${this.baseUrl}/api/v1/products/${id}`);
  }

  getCategories() {
    return this.http.get(`${this.baseUrl}/api/v1/categories`);
  }

  getWishlist() {
    return this.http.get(`${this.baseUrl}/api/v1/wishlist`);
  }

  removeFromWishlist(id: number) {
    return this.http.delete(`${this.baseUrl}/api/v1/wishlist/${id}`);
  }

  addToWishlist(id: number) {
    return this.http.post(`${this.baseUrl}/api/v1/wishlist/${id}`, {});
  }
  getBestSellingProducts() {
    return this.http.get<any[]>(`${this.baseUrl}/api/v1/products`);
  }
  getFlashSaleProducts() {
    return this.http.get<any[]>(`${this.baseUrl}/api/v1/products/flash-sales`);
  } 

}