import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter, withComponentInputBinding, withRouterConfig } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';

import { authInterceptor } from '@eduhub/auth';
import { tenantInterceptor } from '@eduhub/tenant';
import { routes } from './app.routes';
import { errorInterceptor } from './core/error-interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(), 
    provideRouter(
      routes,
      withComponentInputBinding(),
      withRouterConfig({ paramsInheritanceStrategy: 'always' })
    ),
    provideHttpClient(withInterceptors([tenantInterceptor, authInterceptor, errorInterceptor]))],
};
