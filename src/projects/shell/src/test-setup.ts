import '@testing-library/jest-dom/vitest';
import { afterAll, afterEach, beforeAll } from 'vitest';
import { server, reset } from '@eduhub/mocks';

beforeAll(() => server.listen({ onUnhandledFrame: 'error' }));

afterEach(() => {
    server.resetHandlers();
    reset();
});

afterAll(() => server.close());
