import { HttpErrorResponse, HttpInterceptorFn } from "@angular/common/http";
import { tap } from "rxjs"

export const errorInterceptor: HttpInterceptorFn = (req, next) => 
	next(req).pipe(
		tap({
			error: (err: unknown) => {
				if (err instanceof HttpErrorResponse && err.status >= 500) {
					console.error(`[HTTP ${err.status}] ${req.method} ${req.urlWithParams}`);
				}
			}
		})
	)
