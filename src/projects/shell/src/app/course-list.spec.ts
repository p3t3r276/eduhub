import { screen } from '@testing-library/angular';
import { http, HttpResponse } from 'msw';
import { server } from '@eduhub/mocks';
import { renderWithProviders } from '@eduhub/testing';
import { CourseList } from './course-list';