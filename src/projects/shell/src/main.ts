import { isDevMode } from '@angular/core';
import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { App } from './app/app';

async function enableMocking(): Promise<void> {
    if (!isDevMode()) return;
    const { worker, seed }  = await import("@eduhub/mocks");
    seed();
    await worker.start({
        onUnhandledFrame: 'error'
    });
}

enableMocking()
    .then(() => 
bootstrapApplication(App, appConfig).catch((err) => console.error(err)))
    .catch(err => console.error(err));
