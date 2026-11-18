import { TestBed } from "@angular/core/testing";
import { HttpClient, HttpInterceptorFn, provideHttpClient, withInterceptors } from "@angular/common/http";
import { delay, http, HttpResponse } from 'msw';
import { firstValueFrom } from "rxjs";
import { server } from '@eduhub/mocks/node';
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

	it("mọi request có X-Tenant-Id, kể cả request bỏ qua auth", async () => {
		const seen: (string | null)[] = [];

		server.use(http.all('*', ({ request }) => void seen.push(request.headers.get('X-Tenant-Id'))));

		TestBed.inject(TenantService).setTenant('beta');
		await firstValueFrom(httpClient.get('/api/courses'));
		await firstValueFrom(TestBed.inject(AuthService).login('student@eduhub.dev'));

		expect(seen).toEqual(['beta', 'beta'])
	});

	it('3 request đồng thời nhận 401 -> đúng 1 lần /auth/refresh, cả 3 retry thành công', async () => {
		let refreshCalls = 0;
		server.use(
			http.get('/api/courses', ({ request }) => 
				request.headers.get('Authorization') === 'Bearer fresh'
				? HttpResponse.json([])
				: new HttpResponse(null, { status: 401 })
			),
			http.post('/auth/refresh', async () => {
        refreshCalls++;
        await delay(50);
        return HttpResponse.json({ accessToken: 'fresh' });
      }),
		);

		TestBed.inject(AuthService).setSession('expired', { id: 'u1', role: 'student' });

		const results = await Promise.all(
			[1, 2, 3].map(() => firstValueFrom(httpClient.get('/api/courses')))
		)

		expect(results).toEqual([[], [], []]);
		expect(refreshCalls).toBe(1);
	})

	it('refresh lỗi khi báo lỗi, không lặp vô hạn', async () => {
		let refreshCalls = 0;
		server.use(
			http.get('/api/courses', () => new HttpResponse(null, { status: 401 })),
			http.post('/auth/refresh', () => {
				refreshCalls++;
				return new HttpResponse(null, { status: 401 });
			})
		)

		await expect(firstValueFrom(httpClient.get('/api/courses'))).rejects.toMatchObject({ status: 401 });
		expect(refreshCalls).toBe(1);
	})
});
