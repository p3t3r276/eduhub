import { inject } from "@angular/core";
import { AuthService, Role } from "../auth.service";
import { CanMatchFn, Router } from "@angular/router";

export const roleGuard = 
	(...allowed: Role[]): CanMatchFn =>
	() => {
		const role = inject(AuthService).role();
		return role !== null && allowed.includes(role)
			? true
			: inject(Router).createUrlTree(['/forbidden'])
	};
