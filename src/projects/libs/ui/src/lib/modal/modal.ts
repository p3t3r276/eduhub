import { DialogRef } from "@angular/cdk/dialog";
import {
	Component,
	inject,
	input,
} from "@angular/core";

@Component({
	selector: "eh-modal",
	template: `
		<div class="modal">
			<h2>{{ title() }}</h2>
			<ng-content />
			<button type="button" (click)="close()">Đóng</button>
		</div>
	`,
})
export class Modal {
	readonly title = input.required<string>();
	private readonly ref = inject(DialogRef, { optional: true });

	protected close() {
		this.ref?.close();
	}
}
