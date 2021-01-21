import { Component, OnInit,Inject } from '@angular/core';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
import { CookieService } from 'ngx-cookie-service';

export interface DialogData {
  deviceid: string;
}

@Component({
  selector: 'app-deviceid-dialog',
  templateUrl: './deviceid-dialog.component.html',
  styleUrls: ['./deviceid-dialog.component.scss']
})
export class DeviceidDialogComponent implements OnInit {

  deviceid: string;

  constructor(
    public dialogRef: MatDialogRef<DeviceidDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData,
    private cookieService: CookieService) {
      this.deviceid = data.deviceid;
    }


    ngOnInit() {
    }

    save() {
      this.cookieService.set('DeviceID', this.deviceid);
      this.dialogRef.close();
    }

    close() {
      this.dialogRef.close();
    }
}

