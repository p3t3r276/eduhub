import { http, HttpResponse } from 'msw';
import { db } from '../db';

export const coursesHandler = [
    http.get('/api/courses', ({ request }) => {
        const tenantId = request.headers.get('X-Tenant-Id');
        if (!tenantId) {
            return HttpResponse.json({ message: 'Missing X-Tenant-Id header' }, { status: 400 });
        }
        return HttpResponse.json(db.course.findMany({ where: { tenantId: { equals: tenantId } } }));
    }),
];
