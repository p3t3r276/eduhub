import { Component, inject, Injector } from '@angular/core';
import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { RouterTestingHarness } from '@angular/router/testing';
import { provideTenantConfig, readTenantConfig, TENANT_CONFIG } from './tenant.config';

@Component({ template: `{{ config.tenantId }}`})
class Probe {
    config = inject(TENANT_CONFIG);
}

@Component({
    selector: 'scoped-probe',
    providers: [provideTenantConfig({ tenantId: 'gamma' })],
    template: ``
})
class ScopedProbe {
    config = inject(TENANT_CONFIG);
}

describe('TENANT_CONFIG', () => {
    beforeEach(() => {
        TestBed.configureTestingModule({
            providers: [
                provideRouter([
                    { path: 'reports', component: Probe },
                    {
                        path: 't/beta',
                        providers: [provideTenantConfig({
                            tenantId: 'beta', features: { reports: true }
                        })],
                        children: [{ path: 'reports', component: Probe }]
                    }
                ])
            ]
        })
    })

    it('route /t/beta/reports nhận config override', async () => {
        const harness = await RouterTestingHarness.create();
        const probe = await harness.navigateByUrl('/t/beta/reports', Probe);
        expect(probe.config.tenantId).toBe('beta');
        expect(probe.config.features.reports).toBe(true);
        expect(probe.config.currency).toBe('VND');
    });

    it('route khác vẫn nhận default', async () => {
        const harness = await RouterTestingHarness.create();
        const probe = await harness.navigateByUrl('/reports', Probe);
        expect(probe.config.tenantId).toBe('alpha');
    });

    it('providers ở component tạo instance riêng cho component đó', () => {
        const fixture = TestBed.createComponent(ScopedProbe);
        expect(fixture.componentInstance.config.tenantId).toBe('gamma');
        expect(TestBed.inject(TENANT_CONFIG).tenantId).toBe('alpha');
    });

    it('inject() ngoài injection context quăng lỗi NG0203, runInInjectionContext thì được', () => {
        expect(() => inject(TENANT_CONFIG)).toThrow(/NG0203/);
        expect(readTenantConfig(TestBed.inject(Injector)).tenantId).toBe('alpha');
    });
});
