import { Injectable } from '@angular/core';
import { MatDialog } from '@angular/material';
import { CookieService } from 'ngx-cookie-service';
import { Router } from '@angular/router';
import { MatSnackBar, MatSnackBarConfig } from '@angular/material/snack-bar';

@Injectable({
  providedIn: 'root'
})
export class NotificationService {

  public hostName = 'localhost:8000';
  public webSocket;

  constructor(private dialogRef: MatDialog, private cookieService: CookieService,
              private router: Router, private snackBar: MatSnackBar) {
  }

  create(userId) {
    console.log('ws://' + this.hostName + '/ws/notification/' + userId + '/');
    this.webSocket = new WebSocket('ws://' + this.hostName + '/ws/notification/' + userId + '/');
    this.webSocket.onmessage = (e => {
      const data = JSON.parse(e.data);
      const message = data.message;
      console.log(message);
      if (this.cookieService.get('DeviceID')) {
        const deviceId = this.cookieService.get('DeviceID');
        // check if the recipient is me
        if (data.recipient + '' === deviceId + '') {
          if (data.message === 'Reset') {
            this.reset(userId);
          } else {
            this.showNotificationInSnackbar(data.message);
          }
        }
      }
    });
    this.webSocket.onclose = (e => {
      console.log('Chat socket closed');
    });
  }

  sendNotification(item) {
    this.webSocket.send(JSON.stringify(item));
  }

  close() {
    this.webSocket.close();
  }

  reset(userId) {
    this.dialogRef.closeAll();
    this.router.navigate(['/' + userId + '/user', { name: 'user' }]);
  }

  showNotificationInSnackbar(snackMessage) {
    const config = new MatSnackBarConfig();
    config.panelClass = ['snackbar'];
    config.duration = 5000;
    this.snackBar.open(snackMessage, 'close', config);
  }


}
