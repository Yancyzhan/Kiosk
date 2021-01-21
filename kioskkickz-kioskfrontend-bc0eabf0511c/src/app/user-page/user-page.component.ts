import { Component, OnInit, Output } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { ConfigService } from '../services/config.service';


@Component({
  selector: 'app-user-page',
  templateUrl: './user-page.component.html',
  styleUrls: ['./user-page.component.scss']
})

export class UserPageComponent implements OnInit {
  private cookieValue: string;
  userId = -1;
  @Output() config = {};
  result = {};
  colNum = 4;
  serviceList = [
    {
      id: 1,
      name: 'service C',
      label: 'Get access to area C',
      colorClass: 'bg-danger'
    },
    {
      id: 2,
      name: 'service L',
      label: 'Get access to area L',
      colorClass: 'bg-success'
    },
    {
      id: 3,
      name: 'service S',
      label: 'Get access to area S',
      colorClass: 'bg-info'
    },
    {
      id: 4,
      name: 'Councilor Service',
      label: 'Councilor Service',
      colorClass: 'bg-primary'
    }
  ];

  constructor(private router: Router, private route: ActivatedRoute,
              private configService: ConfigService) {
    this.route.paramMap.subscribe(params => {
      const keys = params.keys;
      keys.forEach(key => {
        if (key === 'id') {
          this.userId =  parseInt(params.get('id'));
        } else {
          this.result[key] = params.get(key);
        }
      });
      this.configService.getConfig(this.userId).subscribe(result => {
        console.log(result);
        this.config = result;
      });
    });

    if (this.serviceList.length === 2 || this.serviceList.length === 4) {
      this.colNum = 2;
    } else if (this.serviceList.length % 3 === 0) {
      this.colNum = 3;
    }
   }


  public ngOnInit(): void {
  }

  toService(service) {
    console.log(service.name);
    this.router.navigate(['/' + this.userId]);
  }
}
