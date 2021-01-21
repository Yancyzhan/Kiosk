import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FaceIdentificationComponent } from './face-identification.component';

describe('FaceIdentificationComponent', () => {
  let component: FaceIdentificationComponent;
  let fixture: ComponentFixture<FaceIdentificationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FaceIdentificationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FaceIdentificationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
