import { render, screen } from '@testing-library/angular';
import { FormField } from "./form-field";

const template = `
	<eh-form-field label="Email" controlId="email" [error]="error">
		<input id="email" type="email" />
	</eh-form-field>
`

describe("FormField", () => {
	it("gắn label với control được project vào", async () => {
		await render(template, { imports: [FormField], componentProperties: { error: null } });
		expect(screen.getByLabelText("Email")).toHaveAttribute("id", "email");
	});

	it("Không hiện lỗi khi error rỗng", async () => {
		await render(template, { imports: [FormField], componentProperties: { error: null } });
		expect(screen.queryByRole("alert")).toBeNull();
	});

	it("Hiện lỗi với role alert và id theo controlId", async () => {
		await render(template, {
			imports: [FormField],
			componentProperties: { error: "Email không hợp lệ" }
		});
		const alert = screen.getByRole("alert");
		expect(alert).toHaveTextContent("Email không hợp lệ");
		expect(alert).toHaveAttribute("id", "email-error");
	})
});
