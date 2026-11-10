# EduHub – 28-Day Angular Lab

EduHub is a hands-on, 28-day learning lab for modern Angular (v22). Over four weeks (Oct 26 – Nov 22, 2026) it builds a multi-tenant education platform that runs entirely on mocked APIs (MSW). The finished app has a shell host with 3 micro frontends, a server-side rendered course catalog, a realtime gradebook over a mocked SignalR hub, and tests at every level.

> **Status:** the repository currently contains the lab plan only. The application code is written day by day by following the plan in [`docs/EduHub – Lab Angular 28 days.md`](docs/EduHub%20–%20Lab%20Angular%2028%20days.md) (written in Vietnamese).

## What you will build

- **Shell (host):** layout, authentication, tenant switching and routing. It loads remotes dynamically through a Native Federation manifest.
- **`mfe-catalog`:** a public course catalog with SSR, hydration, SEO metadata (title, Open Graph, JSON-LD) and no double-fetching thanks to the transfer cache.
- **`mfe-learning`:** the student area, with realtime grade updates.
- **`mfe-admin`:** the teacher/admin area, with optimistic grade edits and rollback, and a typed reactive form for creating quizzes.
- **Multi-tenancy:** two tenants (`alpha` and `beta`) with different themes, locales, data and feature flags.
- **Mock backend:** one set of MSW handlers shared by dev, unit tests, SSR and E2E, including a SignalR hub mocked over WebSocket.

## Tech stack

| Area | Choice | Notes |
| --- | --- | --- |
| Framework | Angular v22 | Standalone, zoneless by default; `ng test` runs Vitest |
| Workspace | Angular CLI multi-project | No Nx, so Native Federation schematics work as-is |
| Runtime | Node 22 LTS or newer | Global `WebSocket` is needed for SignalR mock tests |
| Mock API | MSW v2 + `@mswjs/data` | One set of handlers for dev, tests, SSR and E2E |
| Realtime | `@microsoft/signalr` + MSW `ws.link` | Wrapped behind a `RealtimeClient` interface |
| State | `@ngrx/signals` (SignalStore) | No manual `subscribe()` in components |
| Testing | Vitest, Testing Library, RxJS `TestScheduler`, Playwright, axe | Unit, marble, component, E2E and accessibility tests |
| Micro frontends | `@angular-architects/native-federation` | Major version must match Angular |

## Planned repository layout

```text
eduhub/
  projects/
    shell/            host: layout, auth, tenant, routing
    mfe-catalog/      public catalog, SSR
    mfe-learning/     student area
    mfe-admin/        teacher / admin area
    libs/
      ui/ data-access/ auth/ tenant/ util/
      mocks/          MSW handlers, db, scenarios, signalr
      testing/        renderWithProviders, helpers
  e2e/                Playwright
  docs/               lab plan, journal, ADRs, performance notes
```

## Curriculum

| Week | Dates | Topics | End-of-week result |
| --- | --- | --- | --- |
| 0 | Oct 25 | Setup | Empty workspace with a `verify` script |
| 1 | Oct 26 – Nov 1 | Standalone, Signals, DI, functional router, MSW, test setup, CI | Shell runs on MSW; switching tenant changes theme and data; CI runs lint + test + build |
| 2 | Nov 2 – Nov 8 | RxJS flattening operators (marble tests), typeahead, uploads, Signals ↔ RxJS interop, SignalStore, SignalR mock | Students get grades in realtime; teachers edit grades with optimistic update and rollback |
| 3 | Nov 9 – Nov 15 | SSR, transfer cache, SEO, hydration and `@defer`, typed reactive forms, ControlValueAccessor, a11y, performance | Catalog SSR returns real HTML with no double-fetch; Lighthouse before/after numbers |
| 4 | Nov 16 – Nov 22 | Native Federation, shared dependencies, fault isolation, independent deploys, capstone | Shell + 3 independently deployable remotes; capstone "Live Gradebook & Course Catalog" with green CI |

Each day has four parts: **Goal**, **Watch out**, **Commands** and **Done when**. Weekdays take about 1–1.5 hours; weekends take 3–4 hours.

## Getting started

Requirements: Node 22+ and npm.

```bash
npm i -g @angular/cli@22
```

```bash
ng new eduhub --create-application=false --package-manager=npm
```

Then follow the plan from Day 0. Once the workspace exists, the most common commands are:

| Task | Command |
| --- | --- |
| Run the shell | `ng serve shell` |
| Run everything (Week 4) | `npm run start:all` |
| Test one project | `ng test <project> --no-watch` |
| Test with coverage | `ng test <project> --no-watch --coverage` |
| Test a single file | `ng test <project> --include=**/gradebook.store.spec.ts` |
| E2E | `npx playwright test` · `npx playwright test --ui` |
| Find flaky E2E tests | `npx playwright test --repeat-each=5` |
| Build and run SSR | `ng build mfe-catalog && node dist/mfe-catalog/server/server.mjs` |
| Inspect the bundle | `ng build <app> --stats-json`, then `npx esbuild-visualizer --metadata dist/<app>/stats.json --open` |
| Lighthouse | `npx lighthouse <url> --preset=desktop --view` |
| Update Angular | `ng update @angular/core @angular/cli` |
| Pre-commit check | `npm run verify` (lint + test + build) |

In Week 4 the shell runs on port 4200, and the `mfe-learning` and `mfe-admin` remotes run on 4201 and 4202.

## MSW scenarios

| Scenario | How to enable | Used to test |
| --- | --- | --- |
| `happy` | default | Normal flow |
| `slow` | `?scenario=slow` | Loading states, race conditions, timeouts |
| `flaky` | `?scenario=flaky` | Retry, rollback, error messages |
| `unauthorized` | `?scenario=unauthorized` | Token refresh, redirect to login |
| `empty` | `?scenario=empty` | Empty states |
| Hub disconnect | `dropConnections()` | Reconnect and snapshot reload |

## Working conventions

- Run `npm run verify` before every commit, and use [Conventional Commits](https://www.conventionalcommits.org/).
- At the end of each week, tag `week-N` and write a short retro in `docs/journal.md`.
- Record any decision with real alternatives as a short ADR in `docs/decisions.md` (context, choice, reason).
- Until Week 4, keep features under `projects/shell/src/app/features/<area>` with no cross-imports, so each area can later become its own remote.

## Capstone definition of done

- [ ] Shell + 3 remotes, each built and deployed independently, with versions switched through the manifest
- [ ] 2 tenants that differ in theme, locale and feature flags
- [ ] Catalog SSR: raw HTML has content, title, OG tags and JSON-LD; no double-fetch
- [ ] Realtime gradebook over the SignalR mock, with reconnect, backoff and snapshot reload
- [ ] SignalStore, no manual `subscribe()` in components, no NgModules, zoneless
- [ ] Quiz creation form: `FormArray`, cross-field validator, async validator, ControlValueAccessor
- [ ] At least 2 marble tests (typeahead, backoff)
- [ ] E2E: two-user realtime flow, hub disconnect, API 500 rollback; green 5 out of 5 runs
- [ ] E2E for MFE: a dead remote does not crash the shell
- [ ] axe: no `serious` or `critical` issues on the main pages
- [ ] Coverage of `libs/*` ≥ 80%, green CI
- [ ] Complete README, `docs/decisions.md`, `docs/perf.md` and `docs/journal.md`

## References

- [Native Federation on npm](https://npmjs.com/package/@angular-architects/native-federation)
- [Micro Frontends with Modern Angular – Angular In Depth](https://angularindepth.com/article/micro-frontends-with-modern-angular-part-1-standalone-and-esbuild/)
- [Angular release history](https://versionlog.com/angular/)

## License

[MIT](LICENSE) © 2026 p3t3r276
