import { Component, OnInit, Inject } from '@angular/core';
import {MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';


@Component({
  selector: 'app-result-dialog',
  templateUrl: './result-dialog.component.html',
  styleUrls: ['./result-dialog.component.scss']
})
export class ResultDialogComponent implements OnInit {

  imgSrc: any;
  config: any;
  name: string;

  constructor(public dialogRef: MatDialogRef<ResultDialogComponent>,
              @Inject(MAT_DIALOG_DATA) public data: any) {
                this.imgSrc = data.imgSrc;
                this.config = data.config;
  }

  ngOnInit() {
  }

  close(doNext) {
    const retVal = {
      doNext,
      name: this.name
    }
    this.dialogRef.close(retVal);
  }

}
