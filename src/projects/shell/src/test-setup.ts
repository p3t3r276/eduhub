import '@testing-library/jest-dom/vitest';
import { afterAll, afterEach, beforeAll } from 'vitest';
import { server, reset, seed } from '@eduhub/mocks';

beforeAll(() => {
    server.listen({ onUnhandledFrame: 'error' });
    seed();
});

afterEach(() => {
    server.resetHandlers();
    reset();
});

afterAll(() => server.close());
