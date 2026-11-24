import { Dialog } from "@angular/cdk/dialog";
import { ComponentType } from "@angular/cdk/portal";
import { Injectable, inject } from "@angular/core";

@Injectable({ providedIn: 'root' })
export class ModalService {
  private readonly dialog = inject(Dialog);

  open<T>(component: ComponentType<T>, options: { title?: string,  data?: unknown}) {
    return this.dialog.open(component, {
      data: options.data,
      ariaLabel: options.title,
      hasBackdrop: true,
      autoFocus: 'first-tabbable',
      restoreFocus: true,
      closeOnNavigation: true
    })
  }
}
