import { Component, OnInit, Output } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { ConfigService } from '../services/config.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  images = [1, 2, 3].map(() => `https://picsum.photos/900/500?random&t=${Math.random()}`);

  userId = -1;
  @Output() config = {};

  constructor(private configService: ConfigService,
              private router: Router, private route: ActivatedRoute) {
    this.route.paramMap.subscribe(params => {
      // tslint:disable-next-line:radix
      this.userId =  parseInt(params.get('id'));
      this.configService.getConfig(this.userId).subscribe(result => {
        console.log(result);
        this.config = result;
      });
    });
   }

  ngOnInit() {
  }

  start() {
    console.log('start');
    this.router.navigate(['/' + this.userId + '/face']);
  }

}
