import { Component, signal, inject } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { toSignal } from '@angular/core/rxjs-interop';
import { TenantSwitcher } from './tenant-switcher/tenant-switcher';

@Component({
  imports: [RouterOutlet, TenantSwitcher],
  selector: 'app-root',
  styleUrl: './app.scss',
  templateUrl: './app.html',
})
export class App {
  protected readonly title = signal('shell');
  private http = inject(HttpClient);
  courses = toSignal(this.http.get<{ id: string; title: string }[]>('/api/courses', {
    headers: {
      'X-Tenant-Id': 'alpha'
    }
  }))
}
