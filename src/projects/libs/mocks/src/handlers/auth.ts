import { delay, http, HttpResponse } from 'msw';

let seq = 0;

export const authHandlers = [
  http.post('/auth/login', async ({ request  }) => {
    const { email } = (await request.json()) as { email: string };
    const role = email.startsWith('teacher') ? 'teacher' : 'student';
    return HttpResponse.json({ accessToken: `token-${++seq}`, user: { id: email, role } });
  }),
  http.post('/auth/refresh', async () => {
    await delay(50);
    return HttpResponse.json({ accessToken: `token-${++seq}` });
  })
]
