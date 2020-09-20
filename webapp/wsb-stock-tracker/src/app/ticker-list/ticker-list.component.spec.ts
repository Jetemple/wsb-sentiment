import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TickerListComponent } from './ticker-list.component';

describe('TickerListComponent', () => {
  let component: TickerListComponent;
  let fixture: ComponentFixture<TickerListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TickerListComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TickerListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
