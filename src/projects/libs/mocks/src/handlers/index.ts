import { authHandlers } from './auth';
import { coursesHandler } from './courses';

export const handlers = [
    ...coursesHandler, ...authHandlers
];
