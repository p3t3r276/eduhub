import { screen } from '@testing-library/angular';
import { http, HttpResponse } from 'msw';
import { server } from '@eduhub/mocks/node';
import { renderWithProviders } from '@eduhub/testing';
import { CourseList } from './course-list';

describe('CourseList', () => {
    it('render khóa học của tenant alpha từ MSW', async () => {
        await renderWithProviders(CourseList);
        const items = await screen.findAllByRole('listitem');
        expect(items).toHaveLength(5);
        expect(items[0]).toHaveTextContent(/^alpha/);
    });

    it('hiện thông báo lỗi khi API trả 500', async () => {
        server.use(http.get('/api/courses', () => new HttpResponse(null, { status: 500 })));
        await renderWithProviders(CourseList);
        expect(await screen.findByRole('alert')).toBeInTheDocument();
    })
})
