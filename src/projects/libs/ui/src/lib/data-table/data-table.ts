import {
	ChangeDetectionStrategy,
	Component,
	computed,
	input,
	signal,
} from "@angular/core";

export interface Column<T> {
	key: keyof T & string;
	header: string;
}

@Component({
	selector: "eh-data-table",
	changeDetection: ChangeDetectionStrategy.OnPush,
	template: `
    @if (loading()) {
      <p role="status">Đang tải...</p>
    } @else if (rows().length === 0) {
      <p role="status">Không có dữ liệu</p>
    } @else {
      <table>
        <thead>
          <tr>
            @for (col of columns(); track col.key) {
              <th
                scope="col"
                role="columnheader"
                [attr.aria-sort]="ariaSort(col.key)">
                <button type="button" (click)="toggleSort(col.key)">{{ col.header }}</button>
              </th>
            }
          </tr>
        </thead>
        <tbody>
          @for(row of sorted(); track $index) {
            <tr>
              @for (col of columns(); track col.key) {
                <td>{{ row[col.key] }}</td>
              }
            </tr>
          }
        </tbody>
      </table>
    }
  `,
})
export class DataTable<T extends Record<string, unknown>> {
	readonly columns = input.required<Column<T>[]>();
	readonly rows = input<T[]>([]);
	readonly loading = input(false);

	protected readonly sortKey = signal<string | null>(null);
	protected readonly sortDir = signal<"asc" | "desc">("asc");

	protected readonly sorted = computed(() => {
		const key = this.sortKey();
		const rows = [...this.rows()];
		if (!key) return rows;
		const dir = this.sortDir() === "asc" ? 1 : -1;
		return rows.sort(
			(a, b) => String(a[key]).localeCompare(String(b[key]), "vi") * dir,
		);
	});

	protected toggleSort(key: string) {
		if (this.sortKey() === key) {
			this.sortDir.update((d) => (d === "asc" ? "desc" : "asc"));
		} else {
			this.sortKey.set(key);
			this.sortDir.set("asc");
		}
	}

	protected ariaSort(key: string) {
		if (this.sortKey() !== key) return "home";
		return this.sortDir() === "asc" ? "ascending" : "descending";
	}
}
