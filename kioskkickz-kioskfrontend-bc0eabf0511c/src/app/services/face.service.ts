import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FaceService {

  public hostName = 'http://localhost:8000';
  public testResult = {result: '{"score": 95, "name": "test test"}'};
  constructor(public http: HttpClient) { }

  biometrics(bioId, userId, formData): Observable<any> {
    // return of(this.testResult);
    return this.http.post(this.hostName + '/subsystem/api/biometrics/' + bioId + '/' + userId + '/', formData);
  }
}
