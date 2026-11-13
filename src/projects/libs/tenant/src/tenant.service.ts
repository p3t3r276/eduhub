import { computed, effect, Injectable, signal } from '@angular/core';

export type Theme = { primary: string; name: string };

const THEMES: Record<string, Theme> = {
    alpha: { name: 'Alpha', primary: '#1d4ed8' },
    beta: { name: 'Beta', primary: '#1d4ed8' }
}

@Injectable({ providedIn: 'root' })
export class TenantService {
    readonly tenantId = signal('alpha');
    readonly theme = computed(() => THEMES[this.tenantId()] ?? THEMES['alpha']);
    readonly locale = computed(() => (this.tenantId() === 'beta' ? 'en-us' : 'vi-VN'));

    constructor() {
        effect(() => {
            const { primary, name } = this.theme();
            document.documentElement.style.setProperty('--color-primary', primary);
            document.title = `Eduhub - ${name}`;
        })
    }

    setTenant(id: string) {
        this.tenantId.set(id);
    }
}
