import { Routes } from '@angular/router';
import { roleGuard } from '@eduhub/auth';
import { provideTenantConfig, tenantResolver } from '@eduhub/tenant';

const tenantChildren: Routes = [
    { path: '', pathMatch: 'full', redirectTo: 'courses' },
    { path: 'courses', loadComponent: () => import('./course-list').then(m => m.CourseList) },
    { path: 'courses', loadComponent: () => import('./reports/reports').then(m => m.Reports) }
]

export const routes: Routes = [
    { path: '', pathMatch: 'full', redirectTo: 'courses' },
    { path: 'courses', loadComponent: () => import ('./course-list').then(m => m.CourseList) },
    {
        path: 't/beta',
        providers: [provideTenantConfig({ tenantId: 'beta', currency: 'USD', features: { reports: true }})],
        resolve: { tenant: tenantResolver  },
        children: tenantChildren,
    },
    {
        path: 'admin',
        canMatch: [roleGuard('teacher')],
        loadComponent: () => import('./features/admin/admin-home').then((m) => m.AdminHome),
    },
    { path: 'forbidden', loadComponent: () => import('./forbidden').then((m) => m.Forbidden) }
];
