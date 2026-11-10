# -*- coding: utf-8 -*-
"""Sinh sơ đồ kiến trúc EduHub: 1 hình tổng + 1 hình cho mỗi ngày (0..28)."""
import math, os, sys, textwrap
from xml.sax.saxutils import escape as esc

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
os.makedirs(OUT, exist_ok=True)

COLX = [40, 441, 842, 1243, 1644]
BW = 317

# ---------------------------------------------------------------- styles
KIND = {
    "dev":   ("#FFFFFF", "#6B6B6B", None),
    "test":  ("#F3F1EA", "#8A8A8A", "5 4"),
    "app":   ("#DDF2F1", "#138D90", None),
    "lib":   ("#E3EEFA", "#2F6DB5", None),
    "state": ("#F1E6FA", "#8E44AD", None),
    "mock":  ("#FDEBD8", "#D35400", None),
    "data":  ("#FBE3DF", "#C0392B", None),
    "ssr":   ("#DFF1E6", "#2E8B57", None),
}
EDGE = {  # color, dash, marker, legend
    "http":  ("#C0392B", None,  "Data plane: HTTP / WebSocket tới API (do MSW trả lời)"),
    "ctrl":  ("#2F6DB5", "7 4", "Điều khiển: CLI, test runner, CI chạy / build / đo"),
    "di":    ("#7A4FB5", "3 3", "DI / import / đọc signal giữa các khối code"),
    "push":  ("#D35400", None,  "Push: event realtime, effect, HTML render, state"),
    "local": ("#777777", None,  "Nội bộ trong cùng runtime / chuyển tiếp"),
}
NEW = "#E67E22"

# ---------------------------------------------------------------- model
# box: id -> dict(col, y, kind, title, lines=[(day, text)], start, end, zone)
B = {}
def box(i, col, y, kind, title, lines, start, end=99, zone=None, x=None):
    B[i] = dict(id=i, x=COLX[col] if x is None else x, y=y, kind=kind, title=title,
                lines=lines, start=start, end=end, zone=zone)

# zones: id -> dict(label(s), parent, start, end, style)
Z = {}
def zone(i, label, start, end=99, parent=None, style="solid", color="#5B7DB1"):
    Z[i] = dict(id=i, label=label, start=start, end=end, parent=parent, style=style, color=color)

zone("dev", [(0, "Máy dev & CI")], 0, color="#6B6B6B")
zone("browser", [(1, "Trình duyệt · origin :4200")], 1)
zone("shell", [(1, "apps/shell"), (22, "apps/shell · dynamic host (Native Federation)")], 1, parent="browser", style="dash", color="#138D90")
zone("feat", [(9, "shell/src/app/features/ · tách thành remote ở Tuần 4")], 9, 22, parent="browser", style="dash", color="#138D90")
zone("rlearn", [(22, "mfe-learning · remote :4201")], 22, parent="browser", style="dash", color="#138D90")
zone("radmin", [(22, "mfe-admin · remote :4202")], 22, parent="browser", style="dash", color="#138D90")
zone("libs", [(1, "projects/libs · @eduhub/*"), (23, "projects/libs · @eduhub/* (shared singleton)")], 1, parent="browser", style="dash", color="#2F6DB5")
zone("mocks", [(2, "libs/mocks · MSW (dùng chung dev, test, SSR, E2E)")], 2, color="#D35400")
zone("ssr", [(15, "mfe-catalog · SSR :4000 (Node render + hydrate trên trình duyệt)")], 15, color="#2E8B57")
zone("hosts", [(24, "Static host · remote build độc lập")], 24, color="#6B6B6B")

# ---- Col A: dev & CI
box("cli", 0, 160, "dev", "Terminal · Angular CLI v22 + npm", [
    (0, "ng new eduhub --create-application=false"),
    (0, "npm run verify = lint + test + build"),
    (1, "ng serve shell · ng build <app>")], 0, zone="dev")
box("docs", 0, 290, "dev", "docs/", [
    (0, "journal.md · decisions.md (ADR)"),
    (21, "perf.md: Lighthouse trước/sau"),
    (28, "README: sơ đồ, cách chạy, scenario MSW")], 0, zone="dev")
box("vitest", 0, 420, "test", "Vitest + Testing Library", [
    (3, "ng test · setupFiles: listen / reset / close"),
    (3, "query theo role, label"),
    (27, "coverage libs/* ≥ 80%")], 3, zone="dev")
box("testing", 0, 550, "test", "libs/testing · renderWithProviders()", [
    (3, "tenant, user, routes giả cho mỗi test")], 3, zone="dev")
box("marble", 0, 650, "test", "TestScheduler · marble test", [
    (8, "4 flattening operator, virtual time"),
    (9, "typeahead: debounce + hủy request cũ"),
    (14, "lịch backoff 1s, 2s, 4s… tối đa 30s")], 8, zone="dev")
box("pw", 0, 780, "test", "Playwright", [
    (16, "đếm request /api/* sau hydrate"),
    (17, "SEO với javaScriptEnabled: false"),
    (24, "e2e/mfe: route.abort() một remote"),
    (26, "2 context: giáo viên + học sinh")], 16, zone="dev")
box("axe", 0, 925, "test", "axe (vitest-axe + @axe-core/playwright)", [
    (20, "không lỗi serious / critical")], 20, zone="dev")
box("lh", 0, 1025, "test", "Lighthouse + esbuild-visualizer", [
    (21, "LCP, CLS, INP, TBT · budgets trong angular.json")], 21, zone="dev")
box("ci", 0, 1125, "dev", "GitHub Actions · ci.yml", [
    (7, "npm ci → npm run verify"),
    (21, "+ Playwright"),
    (27, "lint → unit + coverage → build tất cả → E2E smoke")], 7, zone="dev")
box("startall", 0, 1255, "dev", "npm run start:all (concurrently)", [
    (25, "shell + 3 remote chạy song song")], 25, zone="dev")

# ---- Col B: shell
box("shell", 1, 190, "app", "Shell app · bootstrapApplication", [
    (1, "zoneless · standalone · OnPush"),
    (1, "router lazy (loadComponent)"),
    (6, "withComponentInputBinding · guard theo role"),
    (25, "theme / locale vi, en / feature flag theo tenant")], 1, zone="shell")
box("switcher", 1, 330, "app", "TenantSwitcher component", [
    (4, "input() / model() / output() · @for track id")], 4, zone="shell")
box("devpanel", 1, 430, "app", "Dev panel (chỉ khi isDevMode)", [
    (13, "pushEvent() · dropConnections()"),
    (13, "?scenario=slow | flaky | unauthorized")], 13, zone="shell")
box("nf", 1, 545, "app", "loadRemoteModule + federation.manifest.json", [
    (22, "manifest đọc lúc chạy, không đóng gói"),
    (23, "shareAll({ singleton, strictVersion })"),
    (24, "đổi URL remote → v2 không build lại shell")], 22, zone="shell")
box("fallback", 1, 675, "app", "Fallback route + timeout", [
    (24, "remote chết / treo → shell vẫn chạy")], 24, zone="shell")

# ---- Col C: features (trong shell) -> remotes
box("f_catalog", 2, 190, "app", "features/catalog · CourseSearch", [
    (9, "debounce → distinct → switchMap"),
    (9, "catchError bên trong switchMap")], 9, 15, zone="feat")
box("f_learn", 2, 305, "app", "features/learning · AssignmentSubmit", [
    (10, "exhaustMap chống double-submit"),
    (10, "upload mergeMap(fn, 3)"),
    (14, "điểm realtime cho học sinh")], 10, 22, zone="feat")
box("f_grade", 2, 435, "app", "features/admin · Gradebook page", [
    (12, "đọc GradebookStore, sửa điểm")], 12, 22, zone="feat")
box("f_quiz", 2, 535, "app", "features/admin · QuizEditor", [
    (19, "typed form · FormArray câu hỏi"),
    (19, "validator chéo + async validator"),
    (20, "dùng Rating (CVA)")], 19, 22, zone="feat")
box("r_learn", 2, 225, "app", "mfe-learning · expose ./routes", [
    (22, "AssignmentSubmit · điểm realtime"),
    (24, "build v1 / v2 deploy độc lập")], 22, zone="rlearn")
box("r_grade", 2, 395, "app", "mfe-admin · Gradebook page", [
    (22, "expose ./routes"),
    (25, "giáo viên sửa điểm → học sinh thấy < 1s")], 22, zone="radmin")
box("r_quiz", 2, 510, "app", "mfe-admin · QuizEditor", [
    (22, "FormArray, async validator, Rating CVA")], 22, zone="radmin")

# ---- Col D: libs
box("alias", 3, 190, "lib", "@eduhub/* path alias (tsconfig)", [
    (1, "trỏ thẳng src/public-api.ts, không qua dist"),
    (23, "lib nội bộ share qua path mapping")], 1, zone="libs")
box("tenant", 3, 305, "lib", "libs/tenant", [
    (4, "TenantService: signal + computed theme"),
    (5, "TENANT_CONFIG InjectionToken, override ở route"),
    (6, "tenantInterceptor → X-Tenant-Id · resolver"),
    (25, "2 tenant: alpha / beta khác theme, locale, flag")], 4, zone="libs")
box("auth", 3, 450, "lib", "libs/auth", [
    (6, "authInterceptor: 401 → refresh single-flight"),
    (6, "roleGuard (functional)")], 6, zone="libs")
box("ui", 3, 565, "lib", "libs/ui", [
    (7, "DataTable · Modal (CDK Overlay) · FormField"),
    (20, "Rating: ControlValueAccessor + aria")], 7, zone="libs")
box("util", 3, 680, "lib", "libs/util · rx helpers", [
    (8, "flattening.spec · bảng operator → khi nào dùng")], 8, zone="libs")
box("classlist", 3, 780, "lib", "data-access · ClassList", [
    (11, "cách A: HttpClient + RxJS + toSignal"),
    (11, "cách B: httpResource + linkedSignal")], 11, zone="libs")
box("store", 3, 895, "state", "data-access · GradebookStore (SignalStore)", [
    (12, "optimistic patchState + rollback snapshot"),
    (14, "nhận event realtime → patch + tải lại snapshot")], 12, zone="libs")
box("rt", 3, 1010, "state", "data-access · RealtimeClient", [
    (13, "interface → Observable<GradeEvent>"),
    (13, "SignalRRealtimeClient (@microsoft/signalr)"),
    (14, "retry backoff RxJS · chỉ chạy isPlatformBrowser")], 13, zone="libs")

# ---- Col E: mocks
box("worker", 4, 160, "mock", "browser.ts · setupWorker", [
    (2, "public/mockServiceWorker.js · start trước bootstrap"),
    (2, "onUnhandledRequest: 'error'"),
    (24, "remote chạy standalone tự đăng ký worker")], 2, zone="mocks")
box("handlers", 4, 290, "mock", "handlers/ (REST)", [
    (2, "courses · thiếu X-Tenant-Id → 400"),
    (6, "auth: login, /auth/refresh"),
    (10, "assignments submit · uploads"),
    (12, "PATCH /grades/:id"),
    (19, "kiểm tra trùng tên quiz → 409"),
    (25, "PATCH thành công → pushEvent('gradeUpdated')")], 2, zone="mocks")
box("db", 4, 465, "data", "db/ · @mswjs/data", [
    (2, "tenant → course → assignment → grade"),
    (2, "seed(db) để test reset được")], 2, zone="mocks")
box("scen", 4, 580, "mock", "scenarios/", [
    (9, "slow: delay() theo từ khóa"),
    (12, "flaky (500), unauthorized (401), empty")], 9, zone="mocks")
box("hub", 4, 695, "mock", "handlers/signalr.ts", [
    (13, "http.post …/negotiate → connectionToken"),
    (13, "ws.link hub: handshake {} + RS, ping {type:6} + RS"),
    (13, "pushEvent() · dropConnections()")], 13, zone="mocks")
box("server", 4, 825, "mock", "server.ts · setupServer (Node)", [
    (3, "dùng trong Vitest"),
    (15, "dùng trong process SSR (chỉ dev/test)")], 3, zone="mocks")

# ---- SSR row
SY = 1260
box("ssrserver", 1, SY, "ssr", "server.mjs · Node SSR", [
    (15, "server.listen() của MSW khi dev"),
    (15, "interceptor nối base URL tuyệt đối")], 15, zone="ssr")
box("rmode", 2, SY, "ssr", "app.routes.server.ts", [
    (15, "/courses Prerender · /courses/:slug Server"),
    (15, "/my Client")], 15, zone="ssr")
box("pages", 1, SY + 120, "ssr", "Catalog pages (chuyển từ shell)", [
    (15, "list + detail + typeahead"),
    (17, "NgOptimizedImage, ảnh LCP priority")], 15, zone="ssr")
box("tcache", 2, SY + 120, "ssr", "HttpTransferCache", [
    (16, "includeHeaders X-Tenant-Id · 0 fetch lại")], 16, zone="ssr")
box("seo", 1, SY + 225, "ssr", "SEO: Title, Meta, JSON-LD", [
    (17, "OG, canonical, Course schema qua DOCUMENT")], 17, zone="ssr")
box("defer", 2, SY + 225, "ssr", "Incremental hydration", [
    (18, "@defer (on viewport; hydrate on viewport)"),
    (18, "afterNextRender cho code chỉ chạy browser")], 18, zone="ssr")

box("hv1", 3, SY, "dev", "learning-v1 · npx serve :5001", [(24, "dist/releases/learning-v1")], 24, zone="hosts")
box("hv2", 4, SY, "dev", "learning-v2 · npx serve :5002", [(24, "manifest trỏ sang đây")], 24, zone="hosts")

# ---------------------------------------------------------------- edges
E = []
def edge(a, b, t, day, label, end=99):
    E.append(dict(a=a, b=b, t=t, day=day, label=label, end=end))

edge("cli", "shell", "ctrl", 1, "ng serve / ng build shell")
edge("shell", "alias", "di", 1, "import @eduhub/* qua path alias")
edge("shell", "worker", "http", 2, "fetch /api/* bị Service Worker chặn")
edge("worker", "handlers", "local", 2, "chuyển request tới handler")
edge("handlers", "db", "http", 2, "query / mutate theo X-Tenant-Id")
edge("vitest", "server", "ctrl", 3, "beforeAll listen · afterEach reset + seed")
edge("vitest", "testing", "di", 3, "render component với provider giả")
edge("server", "handlers", "local", 3, "cùng bộ handler với trình duyệt")
edge("switcher", "tenant", "di", 4, "đọc / ghi signal tenant")
edge("tenant", "shell", "push", 4, "effect: CSS variable theme, document.title")
edge("shell", "tenant", "di", 6, "withInterceptors: tenant → auth → error")
edge("auth", "handlers", "http", 6, "POST /auth/refresh đúng 1 lần cho N request 401")
edge("ci", "vitest", "ctrl", 7, "npm run verify trên mỗi push")
edge("shell", "ui", "di", 7, "DataTable, Modal, FormField")
edge("marble", "util", "ctrl", 8, "marble test cho helper RxJS")
edge("f_catalog", "handlers", "http", 9, "GET /api/courses?q= (switchMap)", end=15)
edge("scen", "handlers", "local", 9, "override delay / lỗi theo scenario")
edge("f_learn", "handlers", "http", 10, "POST submit (exhaustMap) · upload ≤ 3 song song", end=22)
edge("classlist", "handlers", "http", 11, "GET /api/classes (httpResource vs RxJS)")
edge("f_grade", "store", "di", 12, "đọc signal, gọi updateGrade()", end=22)
edge("store", "handlers", "http", 12, "PATCH /grades/:id, lỗi → rollback")
edge("rt", "hub", "http", 13, "negotiate + WebSocket /hubs/grades (JSON protocol)")
edge("devpanel", "hub", "push", 13, "pushEvent / dropConnections bằng tay")
edge("hub", "rt", "push", 14, "gradeUpdated · đứt → retry backoff")
edge("rt", "store", "push", 14, "event → patchState, nối lại → tải snapshot")
edge("cli", "ssrserver", "ctrl", 15, "ng build mfe-catalog && node server.mjs")
edge("ssrserver", "server", "local", 15, "setupServer trong process SSR")
edge("rmode", "pages", "local", 15, "render mode theo route")
edge("ssrserver", "tcache", "push", 16, "ghi response vào TransferState trong HTML")
edge("pw", "pages", "ctrl", 16, "kiểm tra 0 request /api/courses sau hydrate")
edge("pages", "seo", "local", 17, "set title / meta / JSON-LD khi render")
edge("pages", "defer", "local", 18, "review + gợi ý hydrate khi vào viewport")
edge("f_quiz", "handlers", "http", 19, "async validator: tên trùng → 409", end=22)
edge("f_quiz", "ui", "di", 20, "Rating (CVA) trong form", end=22)
edge("axe", "pages", "ctrl", 20, "quét a11y trang catalog và form")
edge("lh", "pages", "ctrl", 21, "đo production build, trung vị 3 lần")
edge("ci", "pw", "ctrl", 21, "thêm Playwright vào CI")
edge("nf", "r_learn", "http", 22, "loadRemoteModule('learning', './routes')")
edge("nf", "r_grade", "http", 22, "loadRemoteModule('admin', './routes')")
edge("r_grade", "store", "di", 22, "đọc store qua shared lib")
edge("r_learn", "rt", "di", 22, "một HubConnection dùng chung")
edge("nf", "alias", "di", 23, "share @angular/*, rxjs, @eduhub/* một lần")
edge("nf", "fallback", "local", 24, "remote lỗi hoặc timeout → fallback")
edge("nf", "hv2", "http", 24, "manifest: learning → :5002/remoteEntry.json")
edge("handlers", "hub", "push", 25, "PATCH thành công → broadcast gradeUpdated")
edge("startall", "shell", "ctrl", 25, "chạy shell + 3 remote")
edge("pw", "shell", "ctrl", 26, "E2E capstone: realtime, hub đứt, API 500 rollback")

# ---------------------------------------------------------------- day captions
DAYS = {
 0: ("Chuẩn bị", "Chỉ có terminal và workspace rỗng. Chưa có app nào; thư mục docs/ chờ ghi ADR và retro."),
 1: ("Dựng workspace và shell", "Shell zoneless đầu tiên, import 7 lib qua path alias @eduhub/*."),
 2: ("MSW: DB giả và handler đầu tiên", "Mọi request /api/* của shell đi vào Service Worker của MSW, đọc DB giả theo tenant."),
 3: ("Khung test: Vitest + MSW + Testing Library", "Test chạy trên Node bằng setupServer, dùng chung bộ handler với trình duyệt."),
 4: ("Signals cốt lõi + TenantService", "Tenant là một signal; theme suy ra bằng computed và đẩy ra DOM bằng effect."),
 5: ("DI chuyên sâu", "TENANT_CONFIG có giá trị mặc định ở root và bị override ở một route con. Không thêm khối mới."),
 6: ("Router functional: interceptor, guard, resolver", "Interceptor gắn X-Tenant-Id và token; 401 gọi refresh đúng một lần."),
 7: ("UI lib, CI", "Bộ UI dùng chung và CI chạy verify trên mỗi push."),
 8: ("Flattening operators bằng marble", "Marble test bằng TestScheduler cho helper RxJS."),
 9: ("Typeahead tìm khóa học", "Feature đầu tiên trong shell; scenario slow dựng race condition có chủ đích."),
 10: ("Nộp bài và upload", "exhaustMap chống double-submit, mergeMap giới hạn 3 upload."),
 11: ("Interop Signals ↔ RxJS", "Cùng một màn danh sách lớp làm theo hai cách để so sánh."),
 12: ("Gradebook SignalStore", "Store điểm với optimistic update; scenario flaky để thử rollback."),
 13: ("SignalR mock bằng MSW", "RealtimeClient nói chuyện với hub giả qua negotiate + WebSocket."),
 14: ("Realtime vào store, reconnect", "Event từ hub vào store; đứt kết nối thì backoff và tải lại snapshot."),
 15: ("App catalog SSR + MSW phía server", "Catalog tách khỏi shell thành app SSR; process Node dùng setupServer."),
 16: ("Transfer cache, chống double-fetch", "Response từ server nằm trong HTML; Playwright kiểm tra client không gọi lại."),
 17: ("SEO, meta, ảnh", "Title, meta, OG và JSON-LD sinh ngay khi render trên server."),
 18: ("Hydration và @defer", "Khối dưới màn hình đầu chỉ hydrate khi cuộn tới."),
 19: ("Typed reactive forms", "QuizEditor với FormArray và async validator gọi MSW."),
 20: ("ControlValueAccessor và a11y", "Rating CVA trong libs/ui; axe quét form và catalog."),
 21: ("Performance và tổng kết", "Đo production build, đặt budgets; CI chạy thêm Playwright."),
 22: ("Native Federation: shell và 2 remote", "features/learning và features/admin rời shell thành 2 remote, nạp qua manifest."),
 23: ("Shared dependencies và state dùng chung", "Angular, RxJS và @eduhub/* chỉ tải một lần cho cả trang."),
 24: ("Cô lập lỗi và deploy độc lập", "Remote lỗi thì fallback; đổi version remote chỉ bằng manifest."),
 25: ("Capstone 1: luồng realtime xuyên MFE", "Giáo viên sửa điểm ở mfe-admin, MSW broadcast, học sinh thấy ở mfe-learning."),
 26: ("Capstone 2: E2E luồng chính và luồng lỗi", "Playwright chạy 2 context song song cho giáo viên và học sinh."),
 27: ("Capstone 3: chất lượng", "CI đầy đủ với coverage gate cho libs/*."),
 28: ("Tài liệu, tự chấm, demo", "README và docs hoàn chỉnh; tag v1.0."),
}

# ---------------------------------------------------------------- helpers
def visible(o, d):
    return o["start"] <= d < o["end"]

def box_lines(b, d):
    return [(dd, t) for dd, t in b["lines"] if dd <= d]

def box_h(b, d):
    return 39 + 15 * len(box_lines(b, d))

def wrap(s, n):
    return textwrap.wrap(s, n) or [""]

def zone_label(z, d):
    lab = z["label"][0][1]
    for dd, t in z["label"]:
        if dd <= d:
            lab = t
    return lab

def text_w(s, size):
    return len(s) * size * 0.56

def bez_pt(p, t):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = p
    mt = 1 - t
    return (mt**3*x0 + 3*mt*mt*t*x1 + 3*mt*t*t*x2 + t**3*x3,
            mt**3*y0 + 3*mt*mt*t*y1 + 3*mt*t*t*y2 + t**3*y3)

# ---------------------------------------------------------------- render
def render(d, overall=False, title=None, sub=None):
    hl = not overall
    vb = {k: b for k, b in B.items() if visible(b, d)}
    ve = [e for e in E if e["day"] <= d < e["end"] and e["a"] in vb and e["b"] in vb]
    focus = set()
    if hl:
        focus = {k for k, b in vb.items() if b["start"] == d or any(dd == d for dd, _ in b["lines"])}
        for e in ve:
            if e["day"] == d:
                focus |= {e["a"], e["b"]}
    def fade(k):
        return "" if (not hl or k in focus) else ' opacity="0.32"'
    used = sorted({b["x"] for b in vb.values()})
    remap = {x: (x if overall else COLX[i]) for i, x in enumerate(used)}
    rect = {k: (remap[b["x"]], b["y"], BW, box_h(b, d)) for k, b in vb.items()}

    # zones: leaf zones from boxes, parents from children
    zr = {}
    def members(zid):
        return [k for k, b in vb.items() if b["zone"] == zid]
    for zid, z in Z.items():
        if not visible(z, d):
            continue
        ms = members(zid)
        if not ms:
            continue
        xs = [rect[m][0] for m in ms]; ys = [rect[m][1] for m in ms]
        xe = [rect[m][0] + rect[m][2] for m in ms]; ye = [rect[m][1] + rect[m][3] for m in ms]
        zr[zid] = [min(xs) - 14, min(ys) - 32, max(max(xe) + 14, min(xs) + 6 + text_w(zone_label(z, d), 12.5) + 14), max(ye) + 16]
    for zid, z in Z.items():
        if z["parent"] is None and visible(z, d):
            kids = [k for k, zz in Z.items() if zz["parent"] == zid and k in zr]
            if kids:
                zr[zid] = [min(zr[k][0] for k in kids) - 14, min(zr[k][1] for k in kids) - 30,
                           max(zr[k][2] for k in kids) + 14, max(zr[k][3] for k in kids) + 14]
    # top-level zone with direct members AND kids not used here

    # ports
    def center(k):
        x, y, w, h = rect[k]; return x + w / 2, y + h / 2
    sides = {}
    plan = []
    for i, e in enumerate(ve):
        (ax, ay), (bx, by) = center(e["a"]), center(e["b"])
        if abs(bx - ax) > 60:
            sa, sb = ("r", "l") if bx > ax else ("l", "r")
            mode = "h"
        else:
            gap = abs(by - ay)
            if gap > 260:
                sa = sb = "r" if rect[e["a"]][0] < max(r[0] for r in rect.values()) else "l"
                mode = "loop"
            else:
                sa, sb = ("b", "t") if by > ay else ("t", "b")
                mode = "v"
        plan.append((e, sa, sb, mode))
        sides.setdefault((e["a"], sa), []).append((i, "a", by if sa in "lr" else bx))
        sides.setdefault((e["b"], sb), []).append((i, "b", ay if sb in "lr" else ax))
    port = {}
    for (k, s), lst in sides.items():
        lst.sort(key=lambda t: t[2])
        x, y, w, h = rect[k]
        n = len(lst)
        for j, (i, end, _) in enumerate(lst):
            f = (j + 1) / (n + 1)
            if s == "r": p = (x + w, y + 12 + (h - 24) * f)
            elif s == "l": p = (x, y + 12 + (h - 24) * f)
            elif s == "t": p = (x + 20 + (w - 40) * f, y)
            else: p = (x + 20 + (w - 40) * f, y + h)
            port[(i, end)] = p

    # canvas size
    allx = [r[2] for r in zr.values()] + [rect[k][0] + BW for k in rect] + [r[0] + 30 + text_w(zone_label(Z[z], d), 12.5) for z, r in zr.items()]
    ally = [r[3] for r in zr.values()] + [rect[k][1] + rect[k][3] for k in rect]
    W = max(1200, max(allx) + 40 if allx else 1200)
    content_bottom = max(ally) if ally else 300

    # relationship list layout
    ncol = 2 if W < 1800 else 3
    colw = (W - 80) / ncol
    chars = int(colw / (11.5 * 0.56)) - 4
    items = []
    for n, e in enumerate(ve, 1):
        a, b = vb[e["a"]], vb[e["b"]]
        head = f"{a['title']} → {b['title']}"
        items.append((n, e, wrap(head, chars), wrap(e["label"], chars)))
    per = math.ceil(len(items) / ncol) if items else 0
    legend_y = content_bottom + 50
    list_y = legend_y + 70
    col_heights = []
    for c in range(ncol):
        hsum = sum(16 * (len(h) + len(l)) + 14 for _, _, h, l in items[c*per:(c+1)*per])
        col_heights.append(hsum)
    H = list_y + 30 + (max(col_heights) if col_heights else 0) + 30

    o = []
    A = o.append
    A(f'<?xml version="1.0" encoding="UTF-8"?>')
    A(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}" font-family="\'Segoe UI\', Arial, sans-serif" font-size="12">')
    if overall:
        pass
    else:
        t, s = DAYS[d]
        title = f"Ngày {d} · {t}"
        sub = s
    A(f'<title>{esc(title)}</title>')
    A('<defs>')
    for k, (c, _, _) in EDGE.items():
        A(f'<marker id="a-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
    A('</defs>')
    A(f'<rect x="0" y="0" width="{W:.0f}" height="{H:.0f}" fill="#FCFAF4"/>')
    A(f'<text x="40" y="42" font-size="22" font-weight="700" fill="#222">{esc(title)}</text>')
    for j, ln in enumerate(wrap(sub, int((W - 80) / (13 * 0.53)))):
        A(f'<text x="40" y="{64 + 18*j}" font-size="13" fill="#555">{esc(ln)}</text>')
    if hl:
        nb = [k for k, b in vb.items() if b["start"] == d]
        nu = [k for k, b in vb.items() if b["start"] < d and any(dd == d for dd, _ in b["lines"])]
        ne = [e for e in ve if e["day"] == d]
        moved = [B[k]["title"] for k in B if B[k]["end"] == d]
        parts = [f"Mới: {len(nb)} khối", f"cập nhật: {len(nu)} khối", f"quan hệ mới: {len(ne)}"]
        if moved:
            parts.append("rời chỗ cũ: " + ", ".join(moved))
        parts.append("khối và mũi tên mờ: đã có từ trước, không đổi trong ngày")
        tx = 40
        A(f'<rect x="{tx}" y="{100}" width="12" height="12" rx="2" fill="#FFFFFF" stroke="{NEW}" stroke-width="3"/>')
        A(f'<text x="{tx+20}" y="{110}" font-size="12" fill="#333">{esc(" · ".join(parts))}</text>')

    # zones (top-level first)
    order = sorted(zr, key=lambda z: 0 if Z[z]["parent"] is None else 1)
    labels = []
    for zid in order:
        x0, y0, x1, y1 = zr[zid]
        z = Z[zid]
        top = z["parent"] is None
        dash = ' stroke-dasharray="5 4"' if z["style"] == "dash" else ""
        fo = "0.6" if top else "0.0"
        sw = "1.6" if top else "1.2"
        isnew = hl and z["start"] == d
        stroke = NEW if isnew else z["color"]
        A(f'<rect x="{x0:.0f}" y="{y0:.0f}" width="{x1-x0:.0f}" height="{y1-y0:.0f}" rx="10" fill="#FFFFFF" fill-opacity="{fo}" stroke="{stroke}" stroke-width="{2.4 if isnew else sw}"{dash}/>')
        labels.append((x0, y0, zone_label(z, d), isnew))

    # boxes
    for k, b in vb.items():
        x, y, w, h = rect[k]
        fill, stroke, dash = KIND[b["kind"]]
        isnew = hl and b["start"] == d
        isupd = hl and not isnew and any(dd == d for dd, _ in b["lines"])
        ds = f' stroke-dasharray="{dash}"' if dash and not isnew else ""
        A(f'<g{fade(k)}>')
        A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{NEW if isnew else stroke}" stroke-width="{3 if isnew else 1.4}"{ds}/>')
        A(f'<text x="{x+12}" y="{y+21}" font-size="12.5" font-weight="700" fill="#222">{esc(b["title"])}</text>')
        for j, (dd, t) in enumerate(box_lines(b, d)):
            newl = hl and dd == d and not isnew
            st = f' font-weight="700" fill="{NEW}"' if newl else ' fill="#555"'
            pre = "+ " if newl else ""
            A(f'<text x="{x+12}" y="{y+40+15*j}" font-size="11"{st}>{esc(pre + t)}</text>')
        if isnew or isupd:
            lab = "MỚI" if isnew else "CẬP NHẬT"
            bw_ = 34 if isnew else 66
            A(f'<rect x="{x+w-bw_-8}" y="{y-9}" width="{bw_}" height="18" rx="9" fill="{NEW if isnew else "#FFFFFF"}" stroke="{NEW}" stroke-width="1.4"/>')
            A(f'<text x="{x+w-8-bw_/2}" y="{y+4}" text-anchor="middle" font-size="10.5" font-weight="700" fill="{"#FFFFFF" if isnew else NEW}">{lab}</text>')
        A('</g>')

    # edges
    circles = []
    for i, (e, sa, sb, mode) in enumerate(plan):
        p0 = port[(i, "a")]; p3 = port[(i, "b")]
        if mode == "h":
            k = min(160, max(40, abs(p3[0] - p0[0]) * 0.45))
            s0 = 1 if sa == "r" else -1; s3 = -1 if sb == "l" else 1
            p1 = (p0[0] + s0 * k, p0[1]); p2 = (p3[0] + s3 * k, p3[1])
        elif mode == "v":
            k = max(30, abs(p3[1] - p0[1]) * 0.45)
            s0 = 1 if sa == "b" else -1
            p1 = (p0[0], p0[1] + s0 * k); p2 = (p3[0], p3[1] - s0 * k)
        else:
            s = 1 if sa == "r" else -1
            p1 = (p0[0] + s * 120, p0[1]); p2 = (p3[0] + s * 120, p3[1])
        c, dash, _ = EDGE[e["t"]]
        isnew = hl and e["day"] == d
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        eop = ' opacity="0.2"' if hl and not isnew else ""
        A(f'<path{eop} d="M{p0[0]:.1f},{p0[1]:.1f} C{p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f} {p3[0]:.1f},{p3[1]:.1f}" fill="none" stroke="{c}" stroke-width="{3 if isnew else 2}"{ds} marker-end="url(#a-{e["t"]})"/>')
        for t in (0.5, 0.42, 0.58, 0.34, 0.66, 0.26, 0.74, 0.18, 0.82, 0.12, 0.88):
            q = bez_pt((p0, p1, p2, p3), t)
            inbox = any(rx - 6 < q[0] < rx + rw + 6 and ry - 6 < q[1] < ry + rh + 6 for rx, ry, rw, rh in rect.values())
            if not inbox and all(math.hypot(q[0]-cx, q[1]-cy) > 24 for cx, cy in circles):
                break
        else:
            for t in (0.5, 0.4, 0.6, 0.3, 0.7):
                q = bez_pt((p0, p1, p2, p3), t)
                if all(math.hypot(q[0]-cx, q[1]-cy) > 24 for cx, cy in circles):
                    break
        circles.append(q)
        e["_c"] = (q, c, isnew)

    for n, e in enumerate(ve, 1):
        (qx, qy), c, isnew = e["_c"]
        A(f'<g{"" if (not hl or isnew) else ' opacity="0.35"'}>')
        A(f'<circle cx="{qx:.1f}" cy="{qy:.1f}" r="10.5" fill="{c if isnew else "#FFFFFF"}" stroke="{c}" stroke-width="1.6"/>')
        A(f'<text x="{qx:.1f}" y="{qy+4:.1f}" text-anchor="middle" font-size="11" font-weight="700" fill="{"#FFFFFF" if isnew else c}">{n}</text>')
        A('</g>')

    # zone labels on top
    for x0, y0, lab, isnew in labels:
        w = text_w(lab, 12.5) + 14
        A(f'<rect x="{x0+8:.0f}" y="{y0+6:.0f}" width="{w:.0f}" height="20" rx="4" fill="#FDFCF8" fill-opacity="0.92"/>')
        A(f'<text x="{x0+14:.0f}" y="{y0+20:.0f}" font-size="12.5" font-weight="700" fill="{NEW if isnew else "#333"}">{esc(lab)}</text>')

    # legend
    lx = 40; ly = legend_y
    used_t = {e["t"] for e in ve}
    for j, (k, (c, dash, txt)) in enumerate([kv for kv in EDGE.items() if kv[0] in used_t]):
        cx = lx + (j % 3) * ((W - 80) / 3)
        cy = ly + (j // 3) * 24
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        A(f'<line x1="{cx:.0f}" y1="{cy}" x2="{cx+40:.0f}" y2="{cy}" stroke="{c}" stroke-width="2"{ds} marker-end="url(#a-{k})"/>')
        A(f'<text x="{cx+50:.0f}" y="{cy+4}" font-size="11.5" fill="#333">{esc(txt)}</text>')
    if hl:
        cx = lx + 2 * ((W - 80) / 3); cy = ly + 24
        A(f'<rect x="{cx:.0f}" y="{cy-8}" width="40" height="16" rx="4" fill="#FFFFFF" stroke="{NEW}" stroke-width="3"/>')
        A(f'<text x="{cx+50:.0f}" y="{cy+4}" font-size="11.5" fill="#333">Viền cam / số đặc = thêm trong ngày · chữ cam = dòng mới</text>')

    A(f'<text x="40" y="{list_y}" font-size="14" font-weight="700" fill="#222">Quan hệ giữa các thành phần (số trên mũi tên)</text>')
    for c in range(ncol):
        yy = list_y + 30
        x = 40 + c * colw
        for n, e, head, lab in items[c*per:(c+1)*per]:
            col = EDGE[e["t"]][0]
            isnew = hl and e["day"] == d
            A(f'<g{"" if (not hl or isnew) else ' opacity="0.5"'}>')
            A(f'<circle cx="{x+10:.0f}" cy="{yy-4}" r="9.5" fill="{col if isnew else "#FFFFFF"}" stroke="{col}" stroke-width="1.5"/>')
            A(f'<text x="{x+10:.0f}" y="{yy}" text-anchor="middle" font-size="10.5" font-weight="700" fill="{"#FFFFFF" if isnew else col}">{n}</text>')
            for ln in head:
                A(f'<text x="{x+28:.0f}" y="{yy}" font-size="11.5" font-weight="700" fill="#333">{esc(ln)}</text>'); yy += 16
            for ln in lab:
                A(f'<text x="{x+28:.0f}" y="{yy}" font-size="11.5" fill="{NEW if isnew else "#333"}">{esc(ln)}</text>'); yy += 16
            yy += 14
            A('</g>')
    A('</svg>')
    return "\n".join(o)

exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "views.py"), encoding="utf-8").read())
for d in range(0, 29):
    open(os.path.join(OUT, f"eduhub-day{d:02d}.svg"), "w").write(render(d))
print("ok", len(os.listdir(OUT)))
