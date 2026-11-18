import { TestBed } from "@angular/core/testing";
import { HttpClient, HttpInterceptorFn, provideHttpClient, withInterceptors } from "@angular/common/http";
import { AuthService, authInterceptor } from "@eduhub/auth";
import { TenantService, tenantInterceptor } from "@eduhub/tenant";

describe("tenant + auth interceptor", () => {
	let httpClient: HttpClient;

	beforeEach(() => {
		TestBed.configureTestingModule({
			providers: [provideHttpClient(withInterceptors([tenantInterceptor, authInterceptor]))]
		});
		httpClient = TestBed.inject(HttpClient);
	});

	it("should be created", () => {
		expect(interceptor).toBeTruthy();
	});
});
