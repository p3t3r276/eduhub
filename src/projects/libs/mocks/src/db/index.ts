import { factory, primaryKey } from '@mswjs/data';
import { faker } from '@faker-js/faker';

export const db = factory({
    course: {
        id: primaryKey(faker.string.uuid),
        tenantId: String,
        title: String,
    },
});

export function seed(d: typeof db = db) {
    for (const tenantId of ['alpha', 'beta']) {
        for (let i = 0; i < 5; i++) {
            d.course.create({ tenantId, title: `${tenantId} - ${faker.lorem.words(3)}` });
        }
    }
}

export function reset(d: typeof db = db) {
    d.course.deleteMany({ where: {} });
    seed(d);
}
