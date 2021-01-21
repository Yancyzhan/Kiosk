import { Component, OnInit, Input, OnChanges, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { Idle, DEFAULT_INTERRUPTSOURCES, AutoResume} from '@ng-idle/core';
import { MatDialog } from '@angular/material/dialog';
import { Keepalive } from '@ng-idle/keepalive';
import { DeviceidDialogComponent } from '../deviceid-dialog/deviceid-dialog.component';
import { CookieService } from 'ngx-cookie-service';
import { NotificationService } from '../services/notification.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit, OnChanges, OnDestroy {
  deviceid: string = null;
  idleState = 'Not started.';
  timedOut = false;
  lastPing?: Date = null;
  @Input() config;
  title = 'Biometric Kiosk';

  userId = -1;

  // clock
  public now: Date = new Date();

  constructor(private router: Router, private idle: Idle, private keepalive: Keepalive,
              private cookieService: CookieService, private dialog: MatDialog,
              public notificationService: NotificationService) {

    // set up clock
    setInterval(() => {
      this.now = new Date();
    }, 1);

    idle.setIdle(55);
    idle.setTimeout(5);
    idle.setInterrupts(DEFAULT_INTERRUPTSOURCES);
    idle.onIdleEnd.subscribe(() => {
      this.idleState = 'No longer idle.';
      console.log('onIdleEnd');
    });
    idle.onTimeout.subscribe(() => {
      this.idleState = 'Timed out!';
      this.timedOut = true;
      console.log('onTimeout');
      this.goHome();
      this.dialog.closeAll();
    });
    idle.onIdleStart.subscribe(() => {
      this.idleState = 'You\'ve gone idle!';
      console.log('onIdleStart');
    });
    idle.onTimeoutWarning.subscribe((countdown) => {
      this.idleState = 'You will time out in ' + countdown + ' seconds!';
      console.log('onTimeoutWarning');
    });

    keepalive.interval(15);

    keepalive.onPing.subscribe(() => {
      this.lastPing = new Date();
    });

    this.reset();
   }

  public ngOnInit(): void {

    if (!this.cookieService.get('DeviceID')) {
      const DeviceIDDialogRef = this.dialog.open(DeviceidDialogComponent, {
        data: {deviceid: this.deviceid},
        disableClose: true
       });
      DeviceIDDialogRef.afterClosed().subscribe(result => {
        this.deviceid = this.cookieService.get('DeviceID');
        console.log(this.deviceid);
      });
    } else {
      this.deviceid = this.cookieService.get('DeviceID');
    }
  }

  ngOnChanges() {
    if (this.config.userId) {
      this.userId = this.config.userId;
      this.notificationService.create(this.userId);
    }
    this.title = this.config.headerTitle;
  }

  ngOnDestroy() {
    this.notificationService.close();
  }

  goHome() {
    if (this.router.url !== '/' + this.userId) {
      this.router.navigate(['/' + this.userId]);
    }
  }

  reset() {
    this.idle.watch();
    this.idleState = 'Started.';
    this.timedOut = false;
    console.log('reset!');
  }

  help() {
    const message = {
      message: 'Need help',
      recipient: 'admin',
      sender: this.cookieService.get('DeviceID')
    };
    this.notificationService.sendNotification(message);
  }
}
