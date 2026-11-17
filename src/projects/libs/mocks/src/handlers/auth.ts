import { delay, http, HttpResponse } from 'msw';

let seq = 0;

export const authHandlers = [
  http.post('/auth/login'), async ({ request }) => {
    const { email } = 
  }
]