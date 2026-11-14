import { Routes } from '@angular/router';
import { provideTenantConfig } from '@eduhub/tenant';

export const routes: Routes = [
    { path: '', pathMatch: 'full', redirectTo: 'courses' },
    { path: 'courses', loadComponent: () => import ('./course-list').then(m => m.CourseList) },
    { path: 'reports', loadComponent: () => import('./reports/reports').then(m => m.Reports) },
    {
        path: 't/beta',
        providers: [provideTenantConfig({ tenantId: 'beta', currency: 'USD', features: { reports: true }})],
        children: [
            { path: 'reports', loadComponent: () => import('./reports/reports').then(m => m.Reports) }
        ]
    }
];
