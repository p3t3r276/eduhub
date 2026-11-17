import { inject } from "@angular/core";
import { ResolveFn } from "@angular/router";
import { TENANT_CONFIG } from '../tenant.config';
import { TenantService } from '../tenant.service';

export const tenantResolver: ResolveFn<boolean> = (route, state) => {
	const id = route.paramMap.get("tenantId") ?? inject(TENANT_CONFIG).tenantId;
	inject(TenantService).setTenant(id);
	return true;
};
