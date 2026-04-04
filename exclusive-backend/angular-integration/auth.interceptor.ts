// ============================================================
// FILE: exclusive-shop/src/app/core/auth.interceptor.ts
// Automatically attaches JWT and handles 401 token refresh
// Register in app.config.ts:  provideHttpClient(withInterceptors([authInterceptor]))
// ============================================================
import { HttpInterceptorFn, HttpRequest, HttpHandlerFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, switchMap, throwError } from 'rxjs';
import { ApiService } from '../services/api.service';
import { Router } from '@angular/router';

export const authInterceptor: HttpInterceptorFn = (req: HttpRequest<unknown>, next: HttpHandlerFn) => {
  const api    = inject(ApiService);
  const router = inject(Router);

  return next(req).pipe(
    catchError((err: HttpErrorResponse) => {
      if (err.status === 401 && !req.url.includes('/auth/')) {
        return api.refreshToken().pipe(
          switchMap(res => {
            const retried = req.clone({
              setHeaders: { Authorization: `Bearer ${res.access_token}` }
            });
            return next(retried);
          }),
          catchError(() => {
            api.logout();
            router.navigate(['/']);
            return throwError(() => err);
          })
        );
      }
      return throwError(() => err);
    })
  );
};
