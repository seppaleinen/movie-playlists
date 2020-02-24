import { AfterViewInit, Component, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class HttpService {
  constructor(private http: HttpClient) {
  }

  getHealth() {
    return this.http.get('/backend/health');
  }
}

@Component({
  selector: 'main-selector',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent {
  title = 'frontend';

  constructor(private service: HttpService) {
    this.service = service;
  }
  
  getHealth() {
    this.service.getHealth()
      .subscribe((resp:string) => {
        console.log("Response: " + resp);
      });
  }

}
