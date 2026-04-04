// ============================================================
// FILE: exclusive-shop/src/app/services/api.service.ts
// Drop this into the Angular project to connect to the backend
// ============================================================
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable, BehaviorSubject, tap } from 'rxjs';

const BASE = 'http://localhost:8000/api/v1';

/* ── Interfaces ─────────────────────────────────────── */
export interface LoginPayload   { username: string; password: string; }
export interface RegisterPayload{ name: string; email: string; password: string; phone?: string; }
export interface AuthToken      { access_token: string; refresh_token: string; token_type: string; user: any; }

export interface ProductListResponse {
  items: any[]; total: number; page: number; size: number; pages: number;
}

export interface CartItem { id: number; quantity: number; color?: string; size?: string; product: any; subtotal: number; }
export interface CartResponse { items: CartItem[]; total: number; item_count: number; }

export interface OrderCreate { shipping_address: string; notes?: string; }

/* ── Service ─────────────────────────────────────────── */
@Injectable({ providedIn: 'root' })
export class ApiService {

  private _token$ = new BehaviorSubject<string | null>(localStorage.getItem('access_token'));
  token$ = this._token$.asObservable();

  constructor(private http: HttpClient) {}

  /* helpers */
  private get headers(): HttpHeaders {
    const token = this._token$.value;
    return token ? new HttpHeaders({ Authorization: `Bearer ${token}` }) : new HttpHeaders();
  }
  private authHeaders() { return { headers: this.headers }; }
  private saveTokens(res: AuthToken) {
    localStorage.setItem('access_token',  res.access_token);
    localStorage.setItem('refresh_token', res.refresh_token);
    this._token$.next(res.access_token);
  }

  get isLoggedIn(): boolean { return !!this._token$.value; }

  /* ── Auth ───────────────────────────────────────────── */
  register(payload: RegisterPayload): Observable<any> {
    return this.http.post(`${BASE}/auth/register`, payload);
  }

  login(payload: LoginPayload): Observable<AuthToken> {
    const form = new HttpParams()
      .set('username', payload.username)
      .set('password', payload.password);
    return this.http.post<AuthToken>(`${BASE}/auth/login`,
      form.toString(),
      { headers: new HttpHeaders({ 'Content-Type': 'application/x-www-form-urlencoded' }) }
    ).pipe(tap(res => this.saveTokens(res)));
  }

  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    this._token$.next(null);
  }

  refreshToken(): Observable<AuthToken> {
    const refresh_token = localStorage.getItem('refresh_token') ?? '';
    return this.http.post<AuthToken>(`${BASE}/auth/refresh`, { refresh_token })
      .pipe(tap(res => this.saveTokens(res)));
  }

  me(): Observable<any> {
    return this.http.get(`${BASE}/auth/me`, this.authHeaders());
  }

  /* ── Products ───────────────────────────────────────── */
  getProducts(params?: {
    page?: number; size?: number; search?: string;
    category_id?: number; flash_sale?: boolean; featured?: boolean;
    min_price?: number; max_price?: number; sort?: string;
  }): Observable<ProductListResponse> {
    let p = new HttpParams();
    if (params) Object.entries(params).forEach(([k,v]) => { if (v != null) p = p.set(k, String(v)); });
    return this.http.get<ProductListResponse>(`${BASE}/products`, { params: p });
  }

  getProduct(id: number): Observable<any> {
    return this.http.get(`${BASE}/products/${id}`);
  }

  getFlashSales(limit = 8): Observable<any[]> {
    return this.http.get<any[]>(`${BASE}/products/flash-sales`, { params: { limit } });
  }

  getFeatured(limit = 8): Observable<any[]> {
    return this.http.get<any[]>(`${BASE}/products/featured`, { params: { limit } });
  }

  getBestSelling(limit = 8): Observable<any[]> {
    return this.http.get<any[]>(`${BASE}/products/best-selling`, { params: { limit } });
  }

  getRelated(productId: number, limit = 4): Observable<any[]> {
    return this.http.get<any[]>(`${BASE}/products/related/${productId}`, { params: { limit } });
  }

  getProductReviews(productId: number): Observable<any[]> {
    return this.http.get<any[]>(`${BASE}/products/${productId}/reviews`);
  }

  addReview(productId: number, payload: { rating: number; title?: string; body: string }): Observable<any> {
    return this.http.post(`${BASE}/products/${productId}/reviews`, payload, this.authHeaders());
  }

  /* ── Categories ─────────────────────────────────────── */
  getCategories(): Observable<any[]> {
    return this.http.get<any[]>(`${BASE}/categories`);
  }

  /* ── Cart ───────────────────────────────────────────── */
  getCart(): Observable<CartResponse> {
    return this.http.get<CartResponse>(`${BASE}/cart`, this.authHeaders());
  }

  addToCart(product_id: number, quantity = 1, color?: string, size?: string): Observable<CartResponse> {
    return this.http.post<CartResponse>(`${BASE}/cart`, { product_id, quantity, color, size }, this.authHeaders());
  }

  updateCartItem(itemId: number, quantity: number): Observable<CartResponse> {
    return this.http.patch<CartResponse>(`${BASE}/cart/${itemId}`, { quantity }, this.authHeaders());
  }

  removeCartItem(itemId: number): Observable<CartResponse> {
    return this.http.delete<CartResponse>(`${BASE}/cart/${itemId}`, this.authHeaders());
  }

  clearCart(): Observable<CartResponse> {
    return this.http.delete<CartResponse>(`${BASE}/cart`, this.authHeaders());
  }

  /* ── Wishlist ───────────────────────────────────────── */
  getWishlist(): Observable<any[]> {
    return this.http.get<any[]>(`${BASE}/wishlist`, this.authHeaders());
  }

  addToWishlist(productId: number): Observable<any[]> {
    return this.http.post<any[]>(`${BASE}/wishlist/${productId}`, {}, this.authHeaders());
  }

  removeFromWishlist(productId: number): Observable<any[]> {
    return this.http.delete<any[]>(`${BASE}/wishlist/${productId}`, this.authHeaders());
  }

  /* ── Orders ─────────────────────────────────────────── */
  checkout(payload: OrderCreate): Observable<any> {
    return this.http.post(`${BASE}/orders/checkout`, payload, this.authHeaders());
  }

  getMyOrders(): Observable<any[]> {
    return this.http.get<any[]>(`${BASE}/orders`, this.authHeaders());
  }

  getOrder(orderId: number): Observable<any> {
    return this.http.get(`${BASE}/orders/${orderId}`, this.authHeaders());
  }

  cancelOrder(orderId: number): Observable<any> {
    return this.http.post(`${BASE}/orders/${orderId}/cancel`, {}, this.authHeaders());
  }

  /* ── User profile ───────────────────────────────────── */
  updateProfile(payload: { name?: string; phone?: string; address?: string }): Observable<any> {
    return this.http.patch(`${BASE}/users/me`, payload, this.authHeaders());
  }

  changePassword(current_password: string, new_password: string): Observable<any> {
    return this.http.post(`${BASE}/users/me/change-password`, { current_password, new_password }, this.authHeaders());
  }
}
