import '@testing-library/jest-dom/vitest';
import { afterAll, afterEach, beforeAll } from 'vitest';
import { reset, seed } from '@eduhub/mocks';
import { server } from '@eduhub/mocks/node';

beforeAll(() => {
    server.listen({ onUnhandledFrame: 'error' });
    seed();
});

afterEach(() => {
    server.resetHandlers();
    reset();
});

afterAll(() => server.close());
