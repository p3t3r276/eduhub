import { render, screen } from "@testing-library/angular";
import userEvent from "@testing-library/user-event";
import { DataTable } from "./data-table";

const columns = [{ key: "name", header: "Tên" }];
const rows = [{ name: "Toán" }, { name: "Anh" }, { name: "Lý" }];

const names = () =>
	screen
		.getAllByRole("row")
		.slice(1)
		.map((r) => r.textContent?.trim());

describe("DataTable", () => {
	it("sắp xếp tăng rồi giảm khi bấm header", async () => {
		await render(DataTable, { inputs: { columns, rows } });
		const header = screen.getByRole("columnheader", { name: "Tên" });

		await userEvent.click(screen.getByRole("button", { name: "Tên" }));
		expect(header).toHaveAttribute("aria-sort", "ascending");
		expect(names()).toEqual(["Anh", "Lý", "Toán"]);

		await userEvent.click(screen.getByRole("button", { name: "Tên" }));
		expect(header).toHaveAttribute("aria-sort", "descending");
		expect(names()).toEqual(["Toán", "Lý", "Anh"]);
	});

	it("hiện empty state", async () => {
		await render(DataTable, { inputs: { columns, rows: [] } });
		expect(screen.getByRole("status")).toHaveTextContent("Không có dữ liệu");
	});

	it("hiện empty state", async () => {
		await render(DataTable, { inputs: { columns, rows: [] } });
		expect(screen.getByRole("status")).toHaveTextContent("Không có dữ liệu");
		expect(screen.queryByRole("table")).toBeNull();
	});

	it("hiện loading state", async () => {
		await render(DataTable, { inputs: { columns, rows: [], loading: true } });
		expect(screen.getByRole("status")).toHaveTextContent("Đang tải");
		expect(screen.queryByRole("table")).toBeNull();
	});
});
