import { ChangeDetectionStrategy, Component } from "@angular/core";
import { RouterLink } from "@angular/router";

@Component({
  selector: 'app-forbidden',
  imports: [RouterLink],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <h1>403 - Forbidden</h1>
    <p>Bạn không có quyền truy cập trang này</p>
    <a routerLink="/courses">Về danh sách khóa học</a>
  `
})
export class Forbidden {}
