import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { FormsModule } from '@angular/forms';
import { MatToolbarModule } from '@angular/material/toolbar';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule } from '@angular/material/dialog';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatCardModule } from '@angular/material/card';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatListModule } from '@angular/material/list';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatExpansionModule } from '@angular/material/expansion';
import {Idle, DEFAULT_INTERRUPTSOURCES} from '@ng-idle/core';
import { MatKeyboardModule } from 'ngx7-material-keyboard';

import { NgIdleKeepaliveModule, Keepalive } from '@ng-idle/keepalive';

import { HeaderComponent } from './header/header.component';
import { HomeComponent } from './home/home.component';
import { RouterModule } from '@angular/router';
import { FaceIdentificationComponent } from './face-identification/face-identification.component';
import { LoadingDialogComponent } from './loading-dialog/loading-dialog.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { ResultDialogComponent } from './result-dialog/result-dialog.component';
import { UserPageComponent } from './user-page/user-page.component';

import { CookieService } from 'ngx-cookie-service';
import { DeviceidDialogComponent } from './deviceid-dialog/deviceid-dialog.component';
@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    HomeComponent,
    FaceIdentificationComponent,
    LoadingDialogComponent,
    ResultDialogComponent,
    UserPageComponent,
    DeviceidDialogComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HttpClientModule,
    MatToolbarModule,
    MatButtonModule,
    MatDialogModule,
    MatProgressSpinnerModule,
    MatCardModule,
    MatTooltipModule,
    MatSnackBarModule,
    MatListModule,
    MatGridListModule,
    NgbModule,
    MatInputModule,
    MatFormFieldModule,
    MatIconModule,
    MatExpansionModule,
    MatKeyboardModule,
    NgIdleKeepaliveModule,
    FormsModule,
    RouterModule.forRoot([])

  ],
  providers: [Keepalive, CookieService],
  bootstrap: [AppComponent],
  entryComponents: [LoadingDialogComponent, ResultDialogComponent, DeviceidDialogComponent]
})
export class AppModule { }
