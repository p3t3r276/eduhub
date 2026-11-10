# -*- coding: utf-8 -*-
# Được exec bên trong gen.py: dựng 2 hình tổng (runtime, test & CI) với model riêng.
_ORIG = (B, E, Z)

# ================================================================ 1. Kiến trúc runtime
B, E, Z = {}, [], {}
zone("browser", [(0, "Trình duyệt · origin :4200")], 0)
zone("shell", [(0, "apps/shell · dynamic host")], 0, parent="browser", style="dash", color="#138D90")
zone("remotes", [(0, "Remote (Native Federation)")], 0, parent="browser", style="dash", color="#138D90")
zone("libs", [(0, "libs/ · shared singleton (tải 1 lần)")], 0, parent="browser", style="dash", color="#2F6DB5")
zone("mocks", [(0, "libs/mocks · MSW")], 0, color="#D35400")
zone("ssr", [(0, "mfe-catalog · SSR :4000")], 0, color="#2E8B57")
zone("hosts", [(0, "Static host · deploy độc lập")], 0, color="#6B6B6B")

box("shell", 0, 190, "app", "Shell · bootstrapApplication", [
    (0, "zoneless · standalone · router lazy"),
    (0, "theme / locale / flag theo tenant")], 0, zone="shell")
box("nf", 0, 315, "app", "loadRemoteModule + manifest.json", [
    (0, "manifest đọc lúc chạy, không build lại shell")], 0, zone="shell")
box("fallback", 0, 425, "app", "Fallback route + timeout", [
    (0, "remote chết / treo → shell vẫn chạy")], 0, zone="shell")

box("r_learn", 1, 300, "app", "mfe-learning · :4201", [
    (0, "nộp bài, upload · điểm realtime")], 0, zone="remotes")
box("r_admin", 1, 410, "app", "mfe-admin · :4202", [
    (0, "Gradebook · QuizEditor (forms, CVA)")], 0, zone="remotes")

box("tenant", 2, 190, "lib", "tenant + auth", [
    (0, "TenantService (signal), TENANT_CONFIG"),
    (0, "interceptor X-Tenant-Id, refresh single-flight")], 0, zone="libs")
box("ui", 2, 315, "lib", "ui · util", [
    (0, "DataTable, Modal, Rating (CVA) · rx helpers")], 0, zone="libs")
box("store", 2, 425, "state", "GradebookStore (SignalStore)", [
    (0, "optimistic update + rollback")], 0, zone="libs")
box("rt", 2, 535, "state", "RealtimeClient → SignalR", [
    (0, "retry backoff · tải lại snapshot")], 0, zone="libs")

box("worker", 3, 190, "mock", "browser.ts · setupWorker", [
    (0, "Service Worker chặn /api/*")], 0, zone="mocks")
box("handlers", 3, 300, "mock", "handlers/ REST + db/", [
    (0, "@mswjs/data theo tenant · scenarios slow/flaky")], 0, zone="mocks")
box("hub", 3, 410, "mock", "signalr.ts · hub giả", [
    (0, "negotiate + ws.link · pushEvent")], 0, zone="mocks")
box("nodesrv", 3, 520, "mock", "server.ts · setupServer (Node)", [
    (0, "dùng trong SSR dev và Vitest")], 0, zone="mocks")

box("ssrserver", 2, 700, "ssr", "server.mjs · Node SSR", [
    (0, "render mode theo route · TransferState")], 0, zone="ssr")
box("pages", 1, 700, "ssr", "Catalog pages (hydrate)", [
    (0, "SEO + JSON-LD · @defer hydrate on viewport")], 0, zone="ssr")
box("hosts", 0, 700, "dev", "learning-v1 :5001 · v2 :5002", [
    (0, "npx serve dist/releases/*")], 0, zone="hosts")

edge("shell", "nf", "local", 0, "route /learning, /admin → loadChildren")
edge("nf", "r_learn", "http", 0, "tải remoteEntry.json + ./routes")
edge("nf", "r_admin", "http", 0, "tải remoteEntry.json + ./routes")
edge("nf", "fallback", "local", 0, "remote lỗi hoặc timeout")
edge("nf", "hosts", "http", 0, "manifest trỏ learning → v2, không build lại shell")
edge("shell", "tenant", "di", 0, "interceptor, guard, theme theo tenant")
edge("r_admin", "store", "di", 0, "giáo viên sửa điểm")
edge("r_learn", "rt", "di", 0, "học sinh nghe gradeUpdated")
edge("tenant", "worker", "http", 0, "mọi /api/* (X-Tenant-Id, Bearer token)")
edge("store", "handlers", "http", 0, "PATCH /grades/:id")
edge("rt", "hub", "http", 0, "negotiate + WebSocket /hubs/grades")
edge("handlers", "hub", "push", 0, "PATCH thành công → broadcast")
edge("hub", "rt", "push", 0, "gradeUpdated")
edge("rt", "store", "push", 0, "patchState, nối lại → tải snapshot")
edge("worker", "handlers", "local", 0, "chuyển request tới handler")
edge("ssrserver", "pages", "push", 0, "HTML có dữ liệu + TransferState")
edge("ssrserver", "nodesrv", "local", 0, "GET /api/courses trên server")
edge("nodesrv", "handlers", "local", 0, "cùng bộ handler")

RT_MODEL = (B, E, Z)

# ================================================================ 2. Test & CI
B, E, Z = {}, [], {}
zone("tools", [(0, "Công cụ test & CI (máy dev + GitHub Actions)")], 0, color="#6B6B6B")
zone("sut", [(0, "Thứ được kiểm tra")], 0, color="#5B7DB1")

box("ci", 0, 160, "dev", "GitHub Actions · ci.yml", [
    (0, "lint → unit + coverage → build tất cả → E2E smoke")], 0, zone="tools")
box("vitest", 0, 275, "test", "Vitest + Testing Library", [
    (0, "renderWithProviders() · query theo role/label"),
    (0, "HTTP thật qua MSW setupServer · server.use()"),
    (0, "coverage libs/* ≥ 80%")], 0, zone="tools")
box("marble", 0, 405, "test", "TestScheduler · marble", [
    (0, "virtual time, không fakeAsync")], 0, zone="tools")
box("pw", 0, 515, "test", "Playwright", [
    (0, "2 context song song · --repeat-each=5"),
    (0, "MSW worker: ?scenario=flaky, ngắt hub")], 0, zone="tools")
box("axe", 0, 625, "test", "axe", [(0, "vitest-axe + @axe-core/playwright")], 0, zone="tools")
box("lh", 0, 735, "test", "Lighthouse + esbuild-visualizer", [(0, "production build · budgets")], 0, zone="tools")


box("libs", 2, 160, "lib", "libs/ tenant, auth, ui, util", [
    (0, "interceptor 401 → 1 lần refresh · CVA · guard")], 0, zone="sut")
box("state", 2, 275, "state", "data-access: store + realtime", [
    (0, "optimistic, rollback, reconnect, race")], 0, zone="sut")
box("apps", 2, 405, "app", "Shell + 2 remote (trình duyệt)", [
    (0, "luồng realtime, remote chết, hub đứt")], 0, zone="sut")
box("catalog", 2, 540, "ssr", "mfe-catalog SSR", [
    (0, "HTML thô có nội dung · 0 double-fetch · @defer")], 0, zone="sut")

edge("ci", "vitest", "ctrl", 0, "npm run verify trên mỗi push")
edge("ci", "pw", "ctrl", 0, "E2E smoke")
edge("vitest", "libs", "ctrl", 0, "unit + component test")
edge("vitest", "state", "ctrl", 0, "optimistic / rollback / pushEvent")
edge("marble", "state", "ctrl", 0, "typeahead hủy request cũ · lịch backoff")
edge("pw", "apps", "ctrl", 0, "giáo viên sửa điểm → học sinh thấy < 1s")
edge("pw", "catalog", "ctrl", 0, "SEO với JS tắt · đếm request /api/*")
edge("axe", "apps", "ctrl", 0, "form QuizEditor")
edge("axe", "catalog", "ctrl", 0, "trang catalog")
edge("lh", "catalog", "ctrl", 0, "LCP, CLS, INP, TBT trước/sau")

TT_MODEL = (B, E, Z)

# ================================================================ render
B, E, Z = RT_MODEL
open(os.path.join(OUT, "eduhub-00-overall.svg"), "w").write(render(
    28, overall=True, title="EduHub · Kiến trúc runtime (sau Ngày 28)",
    sub="Shell nạp 2 remote qua manifest; catalog là app SSR riêng. Mọi HTTP và WebSocket đi vào MSW, "
        "Node dùng setupServer với cùng bộ handler. Quan hệ vẽ ở mức khối chức năng, chi tiết từng ngày xem hình theo ngày."))
B, E, Z = TT_MODEL
open(os.path.join(OUT, "eduhub-00-test-ci.svg"), "w").write(render(
    28, overall=True, title="EduHub · Test & CI (sau Ngày 28)",
    sub="Mỗi công cụ nối tới phần nó kiểm tra. Test HTTP đi qua MSW thật thay vì mock service, "
        "nên interceptor, serialization và scenario lỗi đều được kiểm tra."))
B, E, Z = _ORIG
