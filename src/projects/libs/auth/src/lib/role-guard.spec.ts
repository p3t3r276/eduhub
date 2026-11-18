import { Component } from "@angular/core";
import { provideHttpClient } from "@angular/common/http";
import { TestBed } from "@angular/core/testing";
import { provideRouter, Router } from "@angular/router";
import { RouterTestingHarness } from "@angular/router/testing";
import { AuthService, Role } from "../auth.service";
import { roleGuard } from "./role-guard";

@Component({ template: `Admin` })
class AdminPage {}

@Component({ template: `Forbidden` })
class ForbiddenPage {}

async function navigateAs(role: Role, url: string) {
	TestBed.configureTestingModule({
		providers: [
			provideHttpClient(),
			provideRouter([
				{ path: 'admin', canMatch: [roleGuard('teacher')], component: AdminPage },
				{ path: 'forbidden', component: ForbiddenPage }
			])
		]
	})
	TestBed.inject(AuthService).setSession('t', { id: 'u1', role });
	const harness = await RouterTestingHarness.create();
	await harness.navigateByUrl(url);
	return harness;
}

describe('roleGuard', () => {
	it('chặn student vào /admin', async () => {
		const harness = await navigateAs('student', '/admin');
		expect(TestBed.inject(Router).url).toBe('/forbidden');
		expect(harness.routeNativeElement?.textContent).toContain('Forbidden');
	})

	it('cho teacher vào /admin', async () => {
		const harness = await navigateAs('teacher', '/admin');
		expect(TestBed.inject(Router).url).toBe('/admin');
		expect(harness.routeNativeElement?.textContent).toContain('Admin');
	})
})
