import { ChangeDetectionStrategy, Component, inject } from "@angular/core";
import { HttpClient } from '@angular/common/http';
import { toSignal } from '@angular/core/rxjs-interop';
import { catchError, map, of, startWith } from 'rxjs';

type Course = {
    id: string;
    title: string;
};

type State = {
    courses: Course[];
    error: Boolean;
};

@Component({
    selector: 'app-course-list',
    changeDetection: ChangeDetectionStrategy.OnPush,
    template: `
        @if (state().error) {
        <p role="alert">Không tải được danh sách khóa học</p>
        } @else {
        <ul>
            @for (c of state().courses; track c.id) {
            <li>{{ c.title }}</li>
            }
        </ul>
        }
    `
})
export class CourseList {
    private http = inject(HttpClient);
    state = toSignal(
        this.http.get<Course[]>('/api/courses', {  headers: { 'X-Tenant-Id': 'alpha' } }).pipe(
            map((courses): State => ({ courses, error: false })),
            catchError(() => of<State>({ courses: [], error: true })),
            startWith<State>({ courses: [], error: false })
        ),
        { requireSync: true }
    );
}
