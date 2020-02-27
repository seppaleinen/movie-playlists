import { AfterViewInit, Component, Injectable, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { DataService } from './data.service';
import { Post } from './post';


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
export class MainComponent implements OnInit {
  title = 'frontend';
  post: Post[]

  constructor(private service: HttpService, public dataService: DataService) {
    this.service = service;
    this.dataService = dataService;
  }
  
  getHealth() {
    this.service.getHealth()
      .subscribe((resp:string) => {
        console.log("Response: " + resp);
      });
  }

  ngOnInit() {
    this.dataService.getPosts().subscribe(posts => {
      this.post = posts
      this.dataService.postsData = posts
    });
  }

  onSelectedOption(e) {
    this.getFilteredExpenseList();
  }

  getFilteredExpenseList() {
    if (this.dataService.searchOption.length > 0)
      this.post = this.dataService.filteredListOptions();
    else {
      this.post = this.dataService.postsData;
    }
  }


}
