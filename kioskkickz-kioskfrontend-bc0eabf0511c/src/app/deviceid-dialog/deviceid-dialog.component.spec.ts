import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DeviceidDialogComponent } from './deviceid-dialog.component';

describe('DeviceidDialogComponent', () => {
  let component: DeviceidDialogComponent;
  let fixture: ComponentFixture<DeviceidDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DeviceidDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DeviceidDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
