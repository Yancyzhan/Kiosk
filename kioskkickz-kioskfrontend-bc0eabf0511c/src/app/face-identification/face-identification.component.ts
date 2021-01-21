import { Component, OnInit, ViewChild, ElementRef, AfterViewInit, NgZone, Output } from '@angular/core';
import { FaceService } from '../services/face.service';
import { MatDialog } from '@angular/material/dialog';
import { LoadingDialogComponent } from '../loading-dialog/loading-dialog.component';
import { ResultDialogComponent } from '../result-dialog/result-dialog.component';
import { Router, ActivatedRoute } from '@angular/router';
import { MatSnackBar, MatSnackBarConfig } from '@angular/material/snack-bar';
import { ConfigService } from '../services/config.service';
import { NotificationService } from '../services/notification.service';
import { CookieService } from 'ngx-cookie-service';
import { HeaderComponent } from '../header/header.component';

@Component({
  selector: 'app-face-identification',
  templateUrl: './face-identification.component.html',
  styleUrls: ['./face-identification.component.scss']
})
export class FaceIdentificationComponent implements OnInit, AfterViewInit {

  @ViewChild('video', {static: false})
  public videoEleRef: ElementRef;

  @ViewChild('canvas', {static: false})
  public canvasEleRef: ElementRef;

  @ViewChild('resultCanvas', {static: false})
  public resultCanvasEleRef: ElementRef;

  public video: any;
  public canvas: any;
  public resultCanvas: any;

  public ctx: CanvasRenderingContext2D;
  public resultCtx: CanvasRenderingContext2D;

  public result;
  public dataurl;
  public blob;

  public faceZoneWidth = 400;
  public faceZoneHeight = 450;
  public faceZoneX: number;
  public faceZoneY: number;

  userId = -1;
  @Output() config = {};
  public bioId = 1;

  public trialTimes = 0;

  @ViewChild('header', {static: false}) header: HeaderComponent;

  constructor(private faceService: FaceService,
              public dialog: MatDialog,
              private zone: NgZone,
              private router: Router,
              private route: ActivatedRoute,
              private snackBar: MatSnackBar,
              private configService: ConfigService,
              private cookieService: CookieService) {
                this.route.paramMap.subscribe(params => {
                  // tslint:disable-next-line:radix
                  this.userId =  parseInt(params.get('id'));

                  this.configService.getConfig(this.userId).subscribe(result => {
                    console.log(result);
                    this.config = result;
                    if (this.config['biometricSystem']) {
                      this.bioId = this.config['biometricSystem'];
                    }
                    console.log(this.config, this.bioId);
                  });
                });
  }

  ngOnInit() {
  }

  public ngAfterViewInit() {
    this.video = this.videoEleRef.nativeElement;
    this.canvas = this.canvasEleRef.nativeElement;
    this.resultCanvas = this.resultCanvasEleRef.nativeElement;
    this.ctx = this.canvas.getContext( '2d' );
    this.resultCtx = this.resultCanvas.getContext( '2d' );
    this.startCamera();
    console.log("test");
  }

  startCamera() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
        console.log(stream);
        this.video.srcObject = stream;
        this.video.play();
        this.video.addEventListener( 'loadeddata', () => {
          this.canvas.height = this.video.videoHeight;
          this.canvas.width = this.video.videoWidth;
          this.faceZoneWidth = this.video.videoWidth * 0.3;
          this.faceZoneHeight = this.video.videoHeight * 0.6;
          this.faceZoneX = (this.video.videoWidth - this.faceZoneWidth) / 2;
          this.faceZoneY = (this.video.videoHeight - this.faceZoneHeight) / 2;
          this.resultCanvas.width = this.faceZoneWidth;
          this.resultCanvas.height = this.faceZoneHeight;
        } );
        this.zone.runOutsideAngular( () => this.update() );
      });
    }
  }

  faceIdentify() {
    this.resultCtx.drawImage(this.video, this.faceZoneX, this.faceZoneY,
      this.faceZoneWidth, this.faceZoneHeight,
      0, 0, this.faceZoneWidth, this.faceZoneHeight);
    const dataurl = this.resultCanvas.toDataURL('image/png');
    const resultDialogRef = this.dialog.open(ResultDialogComponent, {
      width: this.video.videoWidth * 1 + 'px',
      disableClose: true,
      data: {
        imgSrc: dataurl,
        config: this.config,
      }
    });
    this.resultCanvas.toBlob((blob) => {
      console.log(blob);
      resultDialogRef.afterClosed().subscribe(retVal => {
        const doNext = retVal.doNext;
        console.log(doNext);
        if (doNext) {
          const loadingDialogRef = this.dialog.open(LoadingDialogComponent, {
            data: {message: 'Identifying...'},
            disableClose: true
          });
          const fd = new FormData();
          fd.append('image', blob, 'test.jpg');
          fd.append('title', 'faceIdentification');
          if (this.config['needName']) {
            fd.append('name', retVal.name);
          }
          this.faceService.biometrics(this.bioId, this.userId, fd).subscribe(result => {
            loadingDialogRef.close();
            this.result = result.result;
            this.trialTimes += 1;
            console.log(this.result);
            if (this.result['isAccepted']) {
              this.router.navigate(['/' + this.userId + '/user',
              this.result]);
            } else {
              if (this.trialTimes >= this.config['maxTrialTime']) {
                // Manual identification required
                const message = {
                  message: 'Manual identification required',
                  recipient: 'admin',
                  sender: this.cookieService.get('DeviceID')
                };
                this.header.notificationService.sendNotification(message);
                const blockDialogRef = this.dialog.open(LoadingDialogComponent, {
                  data: {message: 'Manual identification required'},
                  disableClose: true
                });
              } else {
                // try again
                const snackMessage = 'Please, look at the screen and take picture again';
                const config = new MatSnackBarConfig();
                config.panelClass = ['snackbar'];
                config.duration = 5000;
                this.snackBar.open(snackMessage, 'close', config);
              }
            }
          });
        }
      });
    }, 'image/png');
  }

  async update() {
    // Draw the latest frame from the video to canvas
    this.ctx.drawImage( this.video, 0, 0, this.video.videoWidth, this.video.videoHeight );

    // Add message to canvas
    this.addMessage();

    // add face zone
    this.addFaceZone();

    // Request the next frame
    requestAnimationFrame( () => this.update() );
  }

  addMessage() {
    this.ctx.font = '30px Roboto';
    this.ctx.textAlign = 'center';
    this.ctx. textBaseline = 'middle';
    this.ctx.fillStyle = 'white';  // a color name or by using rgb/rgba/hex values
    this.ctx.fillText('Smile! Look at the screen to take picture!',
                      this.canvas.width / 2, this.canvas.height / 15); // text and position
    this.ctx.fillText('Press screen to finalize the picture',
                      this.canvas.width / 2, this.canvas.height / 8); // text and position
  }

  addFaceZone() {
    this.ctx.lineWidth = 5;
    this.ctx.strokeStyle = 'white';
    this.ctx.beginPath();
    this.ctx.rect(this.faceZoneX, this.faceZoneY, this.faceZoneWidth, this.faceZoneHeight);
    this.ctx.stroke();
  }

  cancel() {
    console.log('go back');
    this.router.navigate(['/']);
  }

  // jsonStringClean(str) {
  //   const find = '\'';
  //   const re = new RegExp(find, 'g');
  //   str = str.replace(re, '"');
  //   return str;
  // }
}
