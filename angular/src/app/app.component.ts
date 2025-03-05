import { Component } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';

import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

//import { PostService } from './post.service';

import { ApiComponent } from './api/api.component';
import { AsyncComponent } from './async/async.component';
//import { FormComponent } from './form/form.component';
//import { Form2Component } from './form2/form2.component';
import { Form3Component } from './form3/form3.component';
//import { Form4Component } from './form4/form4.component';
import { HomeComponent } from './home/home.component';
//import { PostComponent } from './post/post.component';
import { TableComponent } from './table/table.component';

@Component({
  selector: 'app-root',
  imports: [
    RouterOutlet,
    RouterLink,
    RouterLinkActive,
    NgbModule,
    ReactiveFormsModule,
    HttpClientModule
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  //title = 'angular-bootstrap';

  components = [
    ApiComponent,
    AsyncComponent,
    //FormComponent,
    //Form2Component,
    Form3Component,
    HomeComponent,
    //PostComponent,
    TableComponent
  ]

  constructor(private modalService: NgbModal) {
  }

}
