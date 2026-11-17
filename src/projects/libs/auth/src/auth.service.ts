import { HttpClient, HttpContext, HttpContextToken } from "@angular/common/http";
import { computed, inject, Injectable, signal } from "@angular/core";
import { finalize, map, Observable, shareReplay, tap } from "rxjs";

export type Role = "student" | "teacher";
export interface User {
  id: string;
  role: Role;
}

export const SKIP_AUTH = new HttpContextToken<boolean>(() => false);

@Injectable({ providedIn: 'root'})
export class AuthService {
  private http = inject(HttpClient);
  private refreshInFlight$: Observable<string> | null = null;

  readonly accessToken = signal<string | null>(null);
  readonly user = signal<User | null>(null);
  readonly role = computed(() => this.user()?.role ?? null);

  setSession(token: string, user: User) {
    this.accessToken.set(token);
    this.user.set(user);
  }

  login(email: string): Observable<User> {
    return this.http.post<{ accessToken: string, user: User }>('/auth/login', { email}, { context: new HttpContext().set(SKIP_AUTH, true)},
    )
    .pipe(
      tap(({ accessToken, user }) => this.setSession(accessToken, user)),
      map(({ user }) => user)
    )
  }

  refresh(): Observable<string> {
    this.refreshInFlight$ ??= this.http.post<{ accessToken: string }>('/auth/refresh', {},{
      context: new HttpContext().set(SKIP_AUTH, true)
    })
    .pipe(
      map(({ accessToken }) => accessToken),
      tap((token) => this.accessToken.set(token)),
      finalize(() => (this.refreshInFlight$ = null)),
      shareReplay({ bufferSize: 1, refCount: true }) // share on http call moathod all subscribers to avoid multiple refresh requests simultaneously.
    );
    return this.refreshInFlight$;
  }
}
