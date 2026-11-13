import { ChangeDetectionStrategy, Component, inject, input, output } from '@angular/core';
import { TenantService } from '@eduhub/tenant';

@Component({
  selector: 'app-tenant-switcher',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <label>
      {{ label() }}
      <select [value]="tenant.tenantId()" (change)="onChange($any($event.target).value)">
        @for (id of tenants(); track id) {
          <option [value]="id">{{ id }}</option>
        }
      </select>
    </label>
  `,
})
export class TenantSwitcher {
  protected tenant = inject(TenantService);
  tenants = input.required<string[]>();
  label = input('Tenant');
  changed = output<string>();

  onChange(id: string) {
    this.tenant.setTenant(id);
    this.changed.emit(id);
  }
}
