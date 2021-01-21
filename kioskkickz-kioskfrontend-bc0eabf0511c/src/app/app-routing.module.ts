import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { FaceIdentificationComponent } from './face-identification/face-identification.component';
import { UserPageComponent } from './user-page/user-page.component';


const routes: Routes = [
  { path: '', redirectTo: '/2', pathMatch: 'full' },
  { path: ':id', component: HomeComponent },
  { path: ':id/face', component: FaceIdentificationComponent },
  { path: ':id/user', component: UserPageComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
