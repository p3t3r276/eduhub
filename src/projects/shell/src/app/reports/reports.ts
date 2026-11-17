import { ChangeDetectionStrategy, Component, inject, input } from '@angular/core';
import { TENANT_CONFIG } from '@eduhub/tenant';

@Component({
  imports: [],
  selector: 'app-reports',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <h2>Báo cáo - {{ config.tenantId }}</h2>
    @if (config.features.reports) {
      <p>Đơn vị tiền tệ: {{ config.currency }}</p>
    } @else {
      <p role="alert">Tenant này chưa bật báo cáo</p>
    }
  `,
})
export class Reports {
  protected readonly config = inject(TENANT_CONFIG);
  readonly tenant = input<string>();
}
