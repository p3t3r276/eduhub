import { inject, InjectionToken, Injector, Provider, runInInjectionContext } from '@angular/core';

export interface TenantConfig {
    tenantId: string;
    currency: string;
    features: { reports: boolean; }
}

export const DEFAULT_TENANT_CONFIG: TenantConfig = {
    tenantId: 'alpha',
    currency: 'VND',
    features: { reports: false }
}

export const TENANT_CONFIG = new InjectionToken<TenantConfig>('TENANT_CONFIG', {
    providedIn: 'root',
    factory: () => DEFAULT_TENANT_CONFIG
});

export function provideTenantConfig(override: Partial<TenantConfig>): Provider {
    return {
        provide: TENANT_CONFIG,
        useFactory: (): TenantConfig => ({
            ...(inject(TENANT_CONFIG, { skipSelf: true, optional: true }) ?? DEFAULT_TENANT_CONFIG), 
            ...override,
        })
    }
}

export function readTenantConfig(injector: Injector): TenantConfig {
    return runInInjectionContext(injector, () => inject(TENANT_CONFIG));
}
