import { ChangeDetectionStrategy, Component, inject } from "@angular/core";
import { AuthService } from "@eduhub/auth";

@Component({
  selector: 'app-admin-home',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <h1>Admin</h1>
    <p>Xin chào, {{ auth.user()?.id }}</p>
  `
})
export class AdminHome {
  protected readonly auth = inject(AuthService);
}