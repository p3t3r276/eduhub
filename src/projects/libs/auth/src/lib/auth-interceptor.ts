import { HttpInterceptorFn, HttpErrorResponse, HttpRequest } from "@angular/common/http";
import { inject } from "@angular/core";
import { catchError, switchMap, throwError } from "rxjs";
import { AuthService, SKIP_AUTH } from "../auth.service";

const withToken = (req: HttpRequest<unknown>, token: string | null) => token ? req.clone({ setHeaders: { Authorization: `Bearer ${token}`}}) : req;

export const authInterceptor: HttpInterceptorFn = (req, next) => {
	if (req.context.get(SKIP_AUTH)) return next(req);

	const auth = inject(AuthService);

	return next(withToken(req, auth.accessToken()))
		.pipe(catchError((err: unknown) => {
			if (!(err instanceof HttpErrorResponse) || err.status !== 401) return throwError(() => err);

			return auth.refresh().pipe(switchMap((token) => next(withToken(req, token))));
		}));
};
