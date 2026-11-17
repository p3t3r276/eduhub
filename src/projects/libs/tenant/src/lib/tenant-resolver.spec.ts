import { TestBed } from "@angular/core/testing";
import { ResolveFn } from "@angular/router";
import { tenantResolver } from "./tenant-resolver";

describe("tenantResolver", () => {
	const executeResolver: ResolveFn<boolean> = (...resolverParameters) =>
		TestBed.runInInjectionContext(() => tenantResolver(...resolverParameters));

	beforeEach(() => {
		TestBed.configureTestingModule({});
	});

	it("should be created", () => {
		expect(executeResolver).toBeTruthy();
	});
});
