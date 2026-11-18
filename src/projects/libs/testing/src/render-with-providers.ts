import { Type } from "@angular/core";
import { provideHttpClient, withInterceptors } from "@angular/common/http";
import {
	provideRouter,
	Routes,
	withComponentInputBinding,
} from "@angular/router";
import { render, RenderResult } from "@testing-library/angular";
import { AuthService, authInterceptor } from "@eduhub/auth";
import { TenantService, tenantInterceptor } from "@eduhub/tenant";

export interface RenderOptions {
	tenant?: string;
	user?: { id: string; role: "student" | "teacher" };
	routes?: Routes;
}

export async function renderWithProviders<T>(
	component: Type<T>,
	{ tenant = "alpha", user, routes = [] }: RenderOptions = {},
): Promise<RenderResult<T>> {
	return render(component, {
		providers: [
			provideHttpClient(withInterceptors([tenantInterceptor, authInterceptor])),
			provideRouter(routes, withComponentInputBinding()),
			{
				provide: TenantService,
				useFactory: () => {
					const svc = new TenantService();
					svc.setTenant(tenant);
					return svc;
				},
			},
			{
				provide: AuthService,
				useFactory: () => {
					const svc = new AuthService();
					if (user) svc.setSession("test-token", user);
					return svc;
				},
			},
		],
	});
}
