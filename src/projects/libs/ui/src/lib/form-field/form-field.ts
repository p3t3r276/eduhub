import { Component, input } from "@angular/core";

@Component({
	selector: "eh-form-field",
	template: `
		<label [for]="controlId()">{{ label() }}</label>
		<ng-content />
		@if (error(); as message) {
			<p [id]="controlId() + '-error'" role="alert">{{ message }}</p>
		}
	`,
})
export class FormField {
	readonly label = input.required<string>();
	readonly controlId = input.required<string>();
	readonly error = input<string | null>(null);
}
