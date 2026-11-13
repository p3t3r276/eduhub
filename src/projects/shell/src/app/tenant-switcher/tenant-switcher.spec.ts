import { provideZonelessChangeDetection } from '@angular/core';
import { render, screen } from '@testing-library/angular';
import userEvent from '@testing-library/user-event';
import { TenantService } from '@eduhub/tenant';
import { TenantSwitcher } from './tenant-switcher';

it('chọn beta thì TenantService đổi tenant', async () => {
  const { fixture } = await render(TenantSwitcher, {
    inputs: { tenants: ['alpha', 'beta'] },
    providers: [provideZonelessChangeDetection()],
  });
  await userEvent.selectOptions(screen.getByRole('combobox'), 'beta');
  expect(fixture.debugElement.injector.get(TenantService).tenantId()).toBe('beta');
});
