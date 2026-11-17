import { HttpInterceptorFn } from "@angular/common/http";
import { inject } from "@angular/core";
import { TenantService } from '../tenant.service'

export const tenantInterceptor: HttpInterceptorFn = (req, next) => {
	const tenantId = inject(TenantService).tenantId();
	return next(req.clone({
		setHeaders: {
			'X-Tenant-ID': tenantId
		}
	}));
};
