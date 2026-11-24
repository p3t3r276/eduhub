import { Component, inject } from "@angular/core";
import { fireEvent, render, screen, waitFor } from "@testing-library/angular";
import { Modal } from "./modal";
import { ModalService } from "./modal.service";
import userEvent from "@testing-library/user-event";

@Component({
	imports: [Modal],
	template: `<eh-modal title="Xác nhận"><p>Bạn chắc chứ?</p></eh-modal>`,
})
class ConfirmContent {}

@Component({
	template: `<button type="button" (click)="open()">Mở</button>`,
})
class Host {
	private readonly modal = inject(ModalService);
	open() {
		this.modal.open(ConfirmContent, { title: "Xác nhận" });
	}
}

describe("Modal", () => {
	it("Esc đóng modal và trả focus về nút mở", async () => {
		await render(Host);
		const opener = screen.getByRole("button", { name: "Mở" });

		await userEvent.click(opener);
		expect(
			await screen.findByRole("dialog", { name: "Xác nhận" }),
		).toBeVisible();

		//await userEvent.keyboard('{Escape}');
		fireEvent.keyDown(document.activeElement ?? document.body, {
			key: "Escape",
			code: "Escape",
			keyCode: 27,
		});
		await waitFor(() => expect(screen.queryByRole("dialog")).toBeNull());
		expect(opener).toHaveFocus();
	});

	it("nút Đóng đóng modal và trả focus về nút mở", async () => {
		await render(Host);
		const opener = screen.getByRole("button", { name: "Mở" });

		await userEvent.click(opener);
		expect(
			await screen.findByRole("dialog", { name: "Xác nhận" }),
		).toBeVisible();

		await userEvent.click(screen.getByRole("button", { name: "Đóng" }));
		expect(screen.queryByRole("dialog")).toBeNull();
		expect(opener).toHaveFocus();
	});
});
