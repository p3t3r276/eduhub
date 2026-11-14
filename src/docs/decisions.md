## ADR-001: Chỗ đặt provider cho cấu hình theo tenant (30/10)

**Bối cảnh:** cần config mặc định cho cả app, nhưng một nhánh route (`/t/beta/...`) cần giá trị khác.

**Quyết định:**
- `TENANT_CONFIG` là `InjectionToken` với `providedIn: 'root'` + `factory` → default, tree-shakable.
- Override bằng `providers` ở route cha (`provideTenantConfig`), không đặt ở component.
- `provideTenantConfig` merge với config của injector cha (`skipSelf`), chỉ ghi đè phần cần đổi.

| Chỗ đặt | Injector | Vòng đời | Dùng khi |
|---|---|---|---|
| `providedIn: 'root'` | Root EnvironmentInjector | Singleton suốt app | Default, service dùng chung |
| `providers` ở route | EnvironmentInjector con của route | Tạo lần đầu vào route, **không** hủy khi rời route | Config/service cho một nhánh route, lazy feature |
| `providers` ở component | NodeInjector của component | Mỗi instance component một bản, hủy theo component | State cục bộ của một cây component |

**Hệ quả:** route con mới dưới `t/beta` tự nhận override. Nếu cần hủy state khi rời route thì dùng provider ở component, không dùng route.
