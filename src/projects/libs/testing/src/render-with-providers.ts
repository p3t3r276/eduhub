import { Type } from '@angular/core';
import { provideHttpClient } from '@angular/common/http';
import { provideRouter, Routes } from '@angular/router';
import { render, RenderResult } from '@testing-library/angular';

export interface RenderOptions {
    tenant?: string;
    user?: { id: string; role: 'student' | 'teacher' };
    routes?: Routes;
}

export async function renderWithProviders<T>(
    component: Type<T>,
    { tenant = 'alpha', user, routes = [] }: RenderOptions = {}
): Promise<RenderResult<T>> {
    return render(component, {
        providers: [
            provideHttpClient(),
            provideRouter(routes),
            { provide: 'TEST_TENANT', useValue: tenant },
            { provide: 'TEST_USER', useValue: user ?? null }
        ]
    });
}
