import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Mocks } from './mocks';

describe('Mocks', () => {
  let component: Mocks;
  let fixture: ComponentFixture<Mocks>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Mocks],
    }).compileComponents();

    fixture = TestBed.createComponent(Mocks);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
