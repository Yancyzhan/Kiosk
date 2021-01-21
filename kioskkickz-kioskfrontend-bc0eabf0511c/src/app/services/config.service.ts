import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ConfigService {

  public hostName = 'http://localhost:8000';
  constructor(public http: HttpClient) { }

  getConfig(id): Observable<any> {
    return this.http.get(this.hostName + '/config/api/configs/' + id);
  }
}
